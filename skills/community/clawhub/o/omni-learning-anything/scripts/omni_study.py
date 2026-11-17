"""Private evidence-derived review. No clock jobs, delivery writes or mastery scores."""
import math
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import omni_core as c
import omni_learning_store as store
import omni_quiz as q
from omni_quiz_schema import require, text, identifier, LIGHT


def preferences(root):
    p = store.path(root, 'review.json')
    value = c.read(p) if p.exists() else {'schema': 1, 'annotations': [], 'settings': {}}
    require(value.get('schema') == 1 and isinstance(value.get('annotations'), list) and isinstance(value.get('settings'), dict), 'Invalid review preferences; preserve for recovery.')
    return value


def clock(root, now=None):
    now = now or datetime.now(timezone.utc)
    require(now.tzinfo is not None, 'Review time must include a timezone.')
    return now.astimezone(ZoneInfo(c.read(root/'config.json')['timezone']))


def at(value):
    result = datetime.fromisoformat(value)
    require(result.tzinfo is not None, 'Observation timestamp needs a timezone.')
    return result


def observations(root):
    """Validate frozen evidence and retain latest grade per answer, never count corrections twice."""
    grouped = {}; versions = {}
    for p in store.quizzes(root):
        d = c.read(p)['definition']; q.quiz(root, d['key'], d['revision'])
        versions[d['key']] = max(versions.get(d['key'], 0), d['revision'])
    for a in store.records(root)['attempts'].values():
        value = q.quiz(root, a['key'], a['revision'])
        require(value['hash'] == a['quiz_hash'], 'Attempt quiz binding changed.')
        d = q.attempt_definition(a, value['definition'])
        lesson, _, state = q.snapshot(root, a['key'])
        require(str(int(a['key'][3:])) in state['lessons'], 'Review requires verified lesson delivery.')
        for question in d['questions']:
            s = q.qstate(a, question)
            events = [e for e in s['events'] if e['kind'] not in ('pause', 'resume')]
            if not events: continue
            identity = 'r_' + store.fingerprint({'quiz': value['hash'], 'question': question['id']})[:24]
            item = grouped.setdefault(identity, {'id': identity, 'key': a['key'], 'revision': a['revision'],
                'question_id': question['id'], 'objective': question['objective'], 'prompt': question['prompt'],
                'source_refs': question['source_refs'], 'sources': [x for x in lesson['sources'] if x['id'] in {r['source_id'] for r in question['source_refs']}],
                'estimated_minutes': max(1, math.ceil(value['definition']['estimated_minutes']/len(value['definition']['questions']))),
                'lightweight': set(question['actions']) <= LIGHT, 'retired': a['revision'] != versions[a['key']],
                '_question': question, '_quiz_hash': value['hash'], '_observations': []})
            latest = max(events, key=lambda e: at(e['at']))
            grade = s['grade']; answer = s['answer']
            if s['status'] == 'revealed': judgment = 'assisted'
            elif s['status'] == 'skipped': judgment = 'unknown'
            elif grade:
                verdict = grade['feedback']['verdict']
                judgment = {'correct': 'assisted' if answer['assisted'] else 'independent', 'incorrect': 'review',
                            'partial': 'review', 'needs_review': 'clarify', 'withdrawn': 'withdrawn'}[verdict]
            else: judgment = 'pending_feedback' if answer else 'unknown'
            # Replacing an answer is not a correction of its historical judgment.
            # Retain the effective grade for every prior answer until that grade is resolved.
            disputes = []
            for prior in [e for e in events if e['kind']=='answer']:
                grades = [e for e in events if e['kind'] in ('feedback','correct') and e['answer_id']==prior['id']]
                effective = grades[-1] if grades else prior if prior.get('feedback') else None
                if effective and effective['feedback']['verdict'] in ('needs_review','withdrawn'):
                    disputes.append({'answer':prior,'grade':effective})
            dispute = max(disputes, key=lambda x:(x['grade']['feedback']['verdict']=='withdrawn',at(x['grade']['at']))) if disputes else None
            if dispute: judgment = 'withdrawn' if dispute['grade']['feedback']['verdict']=='withdrawn' else 'clarify'
            item['_observations'].append({'attempt_id': a['id'], 'question_id': question['id'],
                'answer_id': answer['id'] if answer else None, 'grade_id': grade['id'] if grade else None,
                'at': latest['at'], 'judgment': judgment, 'purpose': a.get('purpose', 'quiz'),
                'answer': answer, 'grade': grade, 'events': events, 'unresolved_disputes':disputes,
                'dispute_evidence': {'attempt_id':a['id'],'question_id':question['id'],'answer_id':dispute['answer']['id'],'grade_id':dispute['grade']['id']} if dispute else None})
    return grouped


def derived(root, now=None):
    root = Path(root).resolve(); local = clock(root, now); prefs = preferences(root); result = []
    for item in observations(root).values():
        obs = sorted(item['_observations'], key=lambda x: (at(x['at']), x['attempt_id']))
        # A skip/silence is unknown, not a replacement for actual prior learning evidence.
        meaningful = [o for o in obs if o['judgment'] != 'unknown']
        latest = (meaningful or obs)[-1]
        # A still-disputed frozen question is not rehabilitated by a later retake.
        disputed = [o for o in obs if o['judgment'] in ('clarify', 'withdrawn')]
        if disputed: latest = sorted(disputed, key=lambda o: (o['judgment']=='withdrawn', at(o['at'])))[-1]
        judgment = latest['judgment']
        independent = 0
        for o in reversed(meaningful):
            if o['judgment'] != 'independent': break
            independent += 1
        interval = min(30, 3 * 2**min(max(independent-1, 0), 4)) if judgment == 'independent' else (1 if judgment == 'assisted' else 0)
        due = at(latest['at']).astimezone(local.tzinfo).date() + timedelta(days=interval)
        notes = [x for x in prefs['annotations'] if x['item_id'] == item['id']]
        controls = [x for x in notes if x['kind'] in ('exclude', 'include')]
        item.update(judgment=judgment, due=due.isoformat() if judgment in ('review','assisted','independent') else None,
            evidence=latest.get('dispute_evidence') or {k:latest[k] for k in ('attempt_id','question_id','answer_id','grade_id')},
            annotations=notes, excluded=bool(controls and controls[-1]['kind']=='exclude'), _observations=obs)
        result.append(item)
    return sorted(result, key=lambda x:(x['key'], x['revision'], x['question_id']))


def public(item): return {k:v for k,v in item.items() if not k.startswith('_')}


def profile(root, now=None):
    return {'items':[public(x) for x in derived(root,now)],
            'note':'Derived observations, not mastery. Self-reports remain separate; silence and skipping are unknown. Retired revisions stay in history.'}


def evidence(root, item_id):
    item = next((x for x in derived(root) if x['id']==item_id), None)
    require(item is not None, 'Unknown review item; inspect the current profile.')
    return dict(public(item), observations=item['_observations'])


def budget(root, minutes):
    total = c.read(Path(root)/'config.json').get('daily_minutes')
    require(type(total) is int and total > 0, 'Agree daily_minutes before planning a shared review budget.')
    require(minutes is None or (type(minutes) is int and 0 <= minutes <= total), 'Review minutes must fit the agreed daily budget.')
    return total


def plan(root, *, mode='balanced', minutes=None, now=None):
    root=Path(root).resolve(); require(mode in ('balanced','new_first','review_only'), 'Choose balanced, new_first or review_only.')
    total=budget(root,minutes); local=clock(root,now)
    if minutes is None: minutes=preferences(root)['settings'].get('daily_review_minutes')
    budget(root,minutes)
    cap=minutes if minutes is not None else (total if mode=='review_only' else min(5,total//3) if mode=='balanced' else min(2,total//5))
    candidates=[x for x in derived(root,now) if not x['retired'] and not x['excluded'] and x['lightweight'] and x['due'] and x['due']<=local.date().isoformat()]
    candidates.sort(key=lambda x:(x['judgment']!='review',x['due'],x['id']))
    chosen=[]; used=0
    for item in candidates:
        if used+item['estimated_minutes']<=cap:
            chosen.append({k:item[k] for k in ('id','key','question_id','objective','estimated_minutes','judgment','source_refs')});used+=item['estimated_minutes']
    return {'mode':mode,'daily_minutes':total,'review_cap_minutes':cap,'review_minutes':used,'new_minutes':0 if mode=='review_only' else total-used,
            'items':chosen,'deferred_items':len(candidates)-len(chosen),
            'note':'Offer only on learner return. Deferred items are not debt. Do not shorten an already approved lesson silently; disclose time conflicts and offer a choice. Heuristic intervals, not a mastery prediction.'}


def annotate(root,item_id,kind,note,event_id):
    root=Path(root).resolve();identifier(event_id)
    require(kind in ('self_report','exclude','include') and text(note), 'Use an actual learner note with self_report, exclude or include. Correct grades through quiz correct.')
    with c.lock(root):
        require(any(x['id']==item_id for x in derived(root)), 'Unknown review item.')
        prefs=preferences(root); payload={'item_id':item_id,'kind':kind,'note':note,'id':event_id}
        old=next((x for x in prefs['annotations'] if x['id']==event_id),None)
        if old: require(all(old[k]==v for k,v in payload.items()), 'Annotation ID conflicts.');return old
        value=dict(payload,at=q.stamp());prefs['annotations'].append(value);store.save(root,('review.json',),prefs);return value


def settings(root, *, minutes):
    root=Path(root).resolve();budget(root,minutes)
    with c.lock(root):
        prefs=preferences(root);prefs['settings']['daily_review_minutes']=minutes;store.save(root,('review.json',),prefs)
        return prefs['settings']


def start(root,item_id,request_id,consent):
    root=Path(root).resolve();identifier(request_id);require(text(consent), 'Review requires the actual learner request.')
    with c.lock(root):
        records=store.records(root);payload={'item_id':item_id,'consent':consent}
        previous=[a for a in records['attempts'].values() if a.get('purpose')=='review']
        for a in previous:
            if request_id in a.get('requests',{}):
                require(a['requests'][request_id]==payload,'Conflicting review request ID.')
                _,a,d=q.load_attempt(root,a['id']);return q.view(a,d)
        item=next((x for x in derived(root) if x['id']==item_id),None)
        require(item and not item['retired'] and not item['excluded'] and item['lightweight'] and item['judgment'] not in ('clarify','withdrawn'), 'Review item is unavailable, disputed, excluded or requires heavy work; inspect evidence first.')
        require(item['estimated_minutes']<=budget(root,None),'Review does not fit the daily budget; agree a new course budget first.')
        for a in reversed(previous):
            if a['review_item']==item_id:
                _,a,d=q.load_attempt(root,a['id'])
                if q.cursor(a,d):
                    a.setdefault('requests',{})[request_id]=payload
                    if q.paused(a):a['events'].append({'id':'resume.'+uuid.uuid4().hex,'kind':'resume','at':q.stamp()})
                    records['attempts'][a['id']]=a;store.save(root,('records.json',),records);return q.view(a,d)
        require(item['judgment'] not in ('pending_feedback','unknown'), 'Finish pending feedback before creating another review attempt.')
        identity=uuid.uuid4().hex
        a={'id':identity,'key':item['key'],'revision':item['revision'],'quiz_hash':item['_quiz_hash'],'purpose':'review',
           'review_item':item_id,'question_ids':[item['question_id']],'request_id':request_id,'consent':consent,
           'requests':{request_id:payload},'created_at':q.stamp(),'events':[]}
        records['attempts'][identity]=a;store.save(root,('records.json',),records)
        return q.view(a,q.attempt_definition(a,q.quiz(root,a['key'],a['revision'])['definition']))


def report(root, *, days=7, now=None):
    root=Path(root).resolve();require(type(days) is int and 1<=days<=366, 'Recap days must be 1–366.')
    local=clock(root,now);since=local.date()-timedelta(days=days-1);items=derived(root,now); observed=[];active=set()
    for item in items:
        for o in item['_observations']:
            answer=o['answer']
            if answer and since<=at(answer['at']).astimezone(local.tzinfo).date()<=local.date():
                observed.append(o);active.add(at(answer['at']).astimezone(local.tzinfo).date().isoformat())
    state=c.read(root/'state.json')
    return {'period':{'from':since.isoformat(),'to':local.date().isoformat()},'observed_study_days':len(active),
        'answered_questions':len(observed),'independent_correct':sum(o['judgment']=='independent' for o in observed),
        'assisted':sum(o['judgment']=='assisted' for o in observed), 'pending_feedback':sum(o['judgment']=='pending_feedback' for o in observed),
        'delivered_lessons':len(state['lessons']), 'delivery_scope':'all_time',
        'items':[public(x) for x in items], 'items_scope':'all_time', 'note':'On-demand recap only. Counts are recorded question attempts, not mastery; delivered lessons are not evidence of study. No automatic weekly task.'}


def forget(root, *, confirm=False):
    require(confirm is True,'Explicit learner confirmation is required to remove review preferences and proposals.')
    root=Path(root).resolve()
    with c.lock(root):
        import shutil
        target=store.path(root,'review.json')
        if target.exists():target.unlink()
        folder=store.path(root,'proposals')
        if folder.exists():shutil.rmtree(folder)
    return {'removed':'review_preferences_and_proposals','note':'Answers, course history and exported copies remain. Use quiz forget for answer deletion; derived judgments disappear with their evidence.'}
