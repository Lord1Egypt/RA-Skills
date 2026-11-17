"""Learner-started assessment; no timers, remote writes or delivery-state changes."""
import copy
import uuid
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
import omni_core as c
import omni_learning_store as store
from omni_quiz_schema import require, text, identifier, key_revision, validate_definition, validate_feedback


def stamp(): return datetime.now(timezone.utc).isoformat()


def snapshot(root, key):
    key_revision(key, 1)
    state = c.read(root/'state.json'); c.check_approval(root, state); c.check_deliveries(root, state)
    manifest = c.reviewed(root, key)
    source = manifest.get('input', f'data/{key}.json'); path = (root/source).resolve()
    require(path.is_relative_to(root) and source in manifest['files'], 'Lesson input must be hash-bound inside this course.')
    lesson = c.read(path)
    config=c.read(root/'config.json')
    if config.get('materials'):
        from omni_materials import validate_source
        for source in lesson['sources']:
            if source.get('material_ref'):validate_source(root,source,config)
    require(lesson.get('day') == int(key[3:]), 'Lesson day does not match this check.')
    binding = {k: c.digest(p) for k, p in {'config': root/'config.json', 'plan': root/'plan.json',
               'manifest': root/'manifests'/f'{key}.json', 'lesson': path}.items()}
    return lesson, binding, state


def quiz(root, key, revision):
    key_revision(key, revision)
    value = c.read(store.path(root, 'quizzes', f'{key}.v{revision}.json'))
    lesson, binding, _ = snapshot(root, key)
    require(value['binding'] == binding, 'Quiz lesson/config binding changed; preserve old records and review a new course/version.')
    require(value['definition']['key'] == key and value['definition']['revision'] == revision, 'Quiz revision mismatch.')
    require(value['hash'] == store.fingerprint({'definition': value['definition'], 'binding': binding}), 'Frozen quiz changed.')
    validate_definition(value['definition'], lesson)
    return value


def prepare(root, definition):
    root = Path(root).resolve()
    with c.lock(root):
        lesson, binding, _ = snapshot(root, definition.get('key'))
        validate_definition(definition, lesson)
        key = definition['key']; revision = definition['revision']
        value = {'definition': definition, 'binding': binding}
        digest = store.fingerprint(value); target = store.path(root, 'quizzes', f'{key}.v{revision}.json')
        if target.exists(): require(c.read(target)['hash'] == digest, 'Frozen revision already exists; prepare a new revision.')
        else: store.save(root, ('quizzes', target.name), dict(value, hash=digest, prepared_at=stamp()))
        return {'key': key, 'revision': revision, 'quiz_hash': digest, 'question_count': len(definition['questions']),
                'estimated_minutes': definition['estimated_minutes'],
                'needs_extra_time_consent': definition['estimated_minutes'] > lesson.get('practice_minutes', 0)}


def qstate(attempt, question):
    events = [e for e in attempt['events'] if e.get('question') == question['id']]
    answers = [e for e in events if e['kind'] == 'answer']
    answer = answers[-1] if answers else None
    grades = [e for e in events if e['kind'] in ('feedback', 'correct') and answer and e['answer_id'] == answer['id']]
    grade = grades[-1] if grades else (answer if answer and answer.get('feedback') else None)
    terminals = [e for e in events if e['kind'] in ('skip', 'reveal')]
    terminal = terminals[-1] if terminals else None
    if terminal and (not answer or events.index(terminal) > events.index(answer)):
        status = 'skipped' if terminal['kind'] == 'skip' else 'revealed'
    else: status = 'graded' if grade else ('awaiting_feedback' if answer else 'pending')
    return {'status': status, 'answer': answer, 'grade': grade, 'events': events}


def summary(attempt, definition):
    states = [qstate(attempt, q) for q in definition['questions']]
    return {'answered': sum(bool(s['answer']) for s in states),
            'skipped': sum(s['status'] == 'skipped' for s in states), 'revealed': sum(s['status'] == 'revealed' for s in states),
            'independent_correct': sum(bool(s['grade'] and s['grade']['feedback']['verdict'] == 'correct' and not s['answer']['assisted']) for s in states),
            'needs_review': sum(bool(s['grade'] and s['grade']['feedback']['verdict'] == 'needs_review') for s in states)}


def cursor(attempt, definition):
    return next((q for q in definition['questions'] if qstate(attempt, q)['status'] in ('pending', 'awaiting_feedback')), None)


def load_attempt(root, attempt_id):
    records = store.records(root)
    require(attempt_id in records['attempts'], 'Unknown attempt; inspect quiz status.')
    attempt = records['attempts'][attempt_id]; value = quiz(root, attempt['key'], attempt['revision'])
    require(attempt['quiz_hash'] == value['hash'], 'Attempt belongs to a different frozen quiz.')
    return records, attempt, attempt_definition(attempt, value['definition'])


def attempt_definition(attempt, definition):
    """Review attempts reuse a frozen question without changing the full quiz."""
    if attempt.get('purpose') != 'review': return definition
    ids = attempt.get('question_ids')
    require(isinstance(ids, list) and len(ids) == 1 and ids[0] in {x['id'] for x in definition['questions']}, 'Review must bind exactly one frozen question.')
    value = copy.deepcopy(definition)
    value['questions'] = [x for x in value['questions'] if x['id'] in ids]
    return value


def paused(attempt):
    events = [e for e in attempt['events'] if e['kind'] in ('pause', 'resume')]
    return bool(events and events[-1]['kind'] == 'pause')


def view(attempt, definition):
    base = {'attempt_id': attempt['id'], 'key': attempt['key'], 'revision': attempt['revision']}
    if paused(attempt): return dict(base, status='paused')
    question = cursor(attempt, definition)
    if question is None: return dict(base, status='complete', summary=summary(attempt, definition))
    state = qstate(attempt, question)
    if state['status'] == 'awaiting_feedback':
        return dict(base, status='needs_feedback', answer_id=state['answer']['id'],
                    grading_context={'question': question, 'raw_answer': state['answer']['raw_answer']})
    public = {k: question[k] for k in ('id', 'kind', 'prompt', 'objective', 'response_hint')}
    if question['kind'] == 'choice': public['options'] = [dict(id=o['id'], text=o['text'], label=chr(65+i)) for i,o in enumerate(question['options'])]
    return dict(base, status='question', question=public, controls=['hint', 'skip', 'reveal', 'pause'])


def start(root, key, request_id, consent, *, revision=None, new_attempt=False, extra_time=False):
    root = Path(root).resolve(); identifier(request_id); require(text(consent), 'Start requires the actual learner request, not silence or a delivery event.')
    with c.lock(root):
        records = store.records(root)
        previous = [a for a in records['attempts'].values() if a['key'] == key and a.get('purpose') != 'review']
        request = {'consent': consent, 'revision': revision, 'new_attempt': new_attempt, 'extra_time': extra_time}
        for a in previous:
            if request_id in a.get('requests', {}):
                require(a['requests'][request_id] == request, 'Conflicting start/resume request ID.')
                return view(a, quiz(root, key, a['revision'])['definition'])
        for a in reversed(previous):
            d = quiz(root, key, a['revision'])['definition']
            if cursor(a, d):
                require(not new_attempt, 'Resume or finish the active attempt before retaking.')
                a.setdefault('requests', {})[request_id] = request
                if paused(a):
                    a['events'].append({'id': 'resume.'+uuid.uuid4().hex, 'kind': 'resume', 'at': stamp()})
                store.save(root, ('records.json',), records)
                return view(a, d)
        if revision is None:
            versions = [c.read(p)['definition']['revision'] for p in store.quizzes(root) if p.name.startswith(key+'.v')]
            require(bool(versions), 'No prepared check for this lesson.')
            revision = max(versions)
        value = quiz(root, key, revision); definition = value['definition']
        lesson, _, state = snapshot(root, key)
        require(str(int(key[3:])) in state['lessons'], 'Start only after verified lesson delivery.')
        require(extra_time or definition['estimated_minutes'] <= lesson.get('practice_minutes', 0), 'Disclose and obtain extra-time consent beyond the original practice budget.')
        if not new_attempt:
            matches = [a for a in previous if a['revision'] == revision]
            if matches:
                matches[-1].setdefault('requests', {})[request_id] = request
                store.save(root, ('records.json',), records)
                return view(matches[-1], definition)
        attempt_id = uuid.uuid4().hex
        attempt = {'id': attempt_id, 'key': key, 'revision': revision, 'quiz_hash': value['hash'], 'request_id': request_id,
                   'consent': consent, 'extra_time': extra_time, 'requests': {request_id: request}, 'created_at': stamp(), 'events': []}
        records['attempts'][attempt_id] = attempt; store.save(root, ('records.json',), records)
        return view(attempt, definition)


def next_question(root, attempt_id):
    root = Path(root).resolve()
    with c.lock(root):
        _, attempt, definition = load_attempt(root, attempt_id)
        return view(attempt, definition)


def question_for(definition, question_id):
    found = next((q for q in definition['questions'] if q['id'] == question_id), None)
    require(found is not None, 'Question is not in this frozen revision.')
    return found


def existing(attempt, event_id, payload):
    identifier(event_id)
    old = next((e for e in attempt['events'] if e['id'] == event_id), None)
    if old: require(all(old.get(k) == v for k,v in payload.items()), 'Event ID conflicts with an existing observation.')
    return old


def append(root, records, attempt, event_id, payload):
    event = dict(payload, id=event_id, at=stamp()); attempt['events'].append(event)
    store.save(root, ('records.json',), records)
    return event


def answer_result(attempt, event):
    return dict(attempt_id=attempt['id'], answer_id=event['id'], assisted=event['assisted'],
                status='answered' if event.get('feedback') else 'needs_feedback', **({'feedback': event['feedback']} if event.get('feedback') else {}))


def normalize_answer(question, answer):
    require(isinstance(answer, dict) and bool(answer) and set(answer) <= {'choice_id', 'text'}, 'Answer uses choice_id and/or raw text only.')
    require(all(text(v) for v in answer.values()), 'Submit a nonempty explicit answer; preselection is not submission.')
    if question['kind'] != 'choice':
        require(set(answer) == {'text'}, 'Text/dialogue responses need raw text.')
        return answer['text']
    options = question['options']; ids = [o['id'] for o in options]
    if 'choice_id' in answer:
        require(answer['choice_id'] in ids, 'Unknown canonical option ID.')
        return answer['choice_id']
    normalized = unicodedata.normalize('NFKC', answer['text']).strip()
    labels = {chr(65+i): o['id'] for i,o in enumerate(options)}
    matches = {o['id'] for o in options if unicodedata.normalize('NFKC', o['text']).strip().casefold() == normalized.casefold()}
    if normalized.upper() in labels: matches.add(labels[normalized.upper()])
    require(len(matches) == 1, 'Ambiguous selection; ask the learner or use an explicit canonical option ID.')
    return next(iter(matches))


def submit(root, attempt_id, question_id, event_id, answer, *, revise=False):
    root = Path(root).resolve()
    with c.lock(root):
        records, attempt, definition = load_attempt(root, attempt_id)
        payload = {'kind': 'answer', 'question': question_id, 'raw_answer': answer, 'revise': revise}
        old = existing(attempt, event_id, payload)
        if old: return answer_result(attempt, old)
        require(not paused(attempt), 'Resume this check before submitting.')
        question = question_for(definition, question_id); state = qstate(attempt, question)
        current = cursor(attempt, definition)
        require((current and current['id'] == question_id) or (revise and state['status'] != 'pending'), 'Answer the current question, or explicitly revise an earlier response.')
        normalized = normalize_answer(question, answer)
        assisted = any(e['kind'] in ('hint', 'reveal', 'feedback', 'correct') or e.get('feedback') for e in state['events'])
        payload.update(normalized_answer=normalized, assisted=bool(assisted))
        if question['kind'] == 'choice':
            option = next(o for o in question['options'] if o['id'] == normalized)
            payload['feedback'] = {'verdict': 'correct' if normalized == question['answer_id'] else 'incorrect',
                                  'explanation': option['feedback']+' '+question['explanation'],
                                  'source_ids': list(dict.fromkeys(r['source_id'] for r in question['source_refs'])),
                                  'next_step': question['response_hint']}
        event = append(root, records, attempt, event_id, payload)
        result = answer_result(attempt, event)
        if question['kind'] != 'choice': result['grading_context'] = {'question': question, 'raw_answer': answer}
        return result


def action(root, attempt_id, question_id, kind, event_id):
    root = Path(root).resolve(); require(kind in ('hint', 'reveal', 'skip', 'pause'), 'Unknown check action.')
    with c.lock(root):
        records, attempt, definition = load_attempt(root, attempt_id)
        payload = {'kind': kind, 'question': question_id}
        old = existing(attempt, event_id, payload)
        if old: return old['result']
        if kind == 'pause': result = {'status': 'paused', 'attempt_id': attempt_id}
        else:
            require(not paused(attempt), 'Resume before continuing.')
            current = cursor(attempt, definition)
            require(current is not None and current['id'] == question_id, 'Act on the current question only.')
            state = qstate(attempt, current)
            if kind == 'hint':
                require(not state['answer'], 'Hints precede submission; revise explicitly after feedback.')
                count = sum(e['kind'] == 'hint' for e in state['events'])
                require(count < len(current['hints']), 'No further prepared hint; offer skip or solution without inventing one.')
                result = {'status': 'hint', 'hint': current['hints'][count], 'attempt_id': attempt_id}
            elif kind == 'reveal':
                solution = next(o['text'] for o in current['options'] if o['id'] == current['answer_id']) if current['kind'] == 'choice' else current['expected_answer']
                result = {'status': 'revealed', 'solution': solution, 'explanation': current['explanation'], 'attempt_id': attempt_id}
            else: result = {'status': 'skipped', 'attempt_id': attempt_id}
        append(root, records, attempt, event_id, dict(payload, result=result))
        return result


def feedback(root, attempt_id, question_id, event_id, answer_id, body):
    return _grade(root, attempt_id, question_id, event_id, body, answer_id=answer_id)


def correct(root, attempt_id, question_id, event_id, replaces, reason, body):
    require(text(reason), 'Correction must retain the learner dispute/review reason.')
    return _grade(root, attempt_id, question_id, event_id, body, replaces=replaces, reason=reason)


def _grade(root, attempt_id, question_id, event_id, body, *, answer_id=None, replaces=None, reason=None):
    root = Path(root).resolve()
    with c.lock(root):
        records, attempt, definition = load_attempt(root, attempt_id)
        payload = {'kind': 'correct' if replaces else 'feedback', 'question': question_id, 'body': body, 'replaces': replaces, 'reason': reason}
        old = existing(attempt, event_id, dict(payload, **({'answer_id': answer_id} if answer_id else {})))
        if old: return {'feedback': old['feedback'], 'event_id': old['id']}
        question = question_for(definition, question_id); state = qstate(attempt, question)
        require(state['answer'] is not None, 'Persist the learner answer before grading.')
        latest = state['answer']['id']
        if replaces: require(state['grade'] and state['grade']['id'] == replaces, 'Correction must name the latest grade; preserve history.')
        else:
            require(question['kind'] != 'choice', 'Choice answers are graded from frozen canonical IDs.')
            require(answer_id == latest and not state['grade'] and state['status'] == 'awaiting_feedback', 'Grading is stale or already recorded; inspect latest response/use correct.')
        verdict = validate_feedback(body, question, correction=bool(replaces))
        result = dict(copy.deepcopy(body), verdict=verdict)
        append(root, records, attempt, event_id, dict(payload, answer_id=latest, feedback=result))
        return {'feedback': result, 'event_id': event_id}


def status(root):
    root = Path(root).resolve()
    with c.lock(root):
        records = store.records(root); attempts = []
        for a in records['attempts'].values():
            value = c.read(store.path(root, 'quizzes', f"{a['key']}.v{a['revision']}.json"))
            attempts.append({'attempt_id': a['id'], 'key': a['key'], 'revision': a['revision'], 'purpose': a.get('purpose', 'quiz'), 'summary': summary(a, attempt_definition(a, value['definition'])), 'paused': paused(a)})
        return {'attempts': attempts, 'prepared': [{'key': c.read(p)['definition']['key'], 'revision': c.read(p)['definition']['revision']} for p in store.quizzes(root)],
                'note': 'Assessment observations only; delivery is separate, silence is unknown, no mastery percentage is inferred.'}
