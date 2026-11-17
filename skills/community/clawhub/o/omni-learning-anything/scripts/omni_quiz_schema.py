"""Frozen question/feedback contracts. Teaching relevance still needs host review."""
import re
import unicodedata

LIGHT = {'select', 'brief_text', 'conversation'}
HEAVY = {'long_writing', 'operate_device', 'write_code', 'experiment', 'project'}


def require(condition, message):
    if not condition: raise ValueError(message)


def text(value): return isinstance(value, str) and bool(value.strip())
def texts(value): return isinstance(value, list) and all(text(x) for x in value)


def identifier(value):
    require(isinstance(value, str) and bool(re.fullmatch(r'[A-Za-z][A-Za-z0-9_.-]{0,95}', value)), 'Use stable non-secret letter-led IDs (letters, digits, dots, hyphens or underscores).')
    return value


def key_revision(key, revision):
    require(isinstance(key, str) and bool(re.fullmatch(r'Day[0-9]{2,}', key)) and int(key[3:]) > 0, 'Checks belong to an explicit DayNN lesson.')
    require(type(revision) is int and 1 <= revision <= 9999, 'Quiz revision must be a positive integer up to 9999.')


def cited_text(value, allowed):
    require(set(re.findall(r'\[(S\d+)\]', value)).issubset(allowed), 'Feedback references an unknown question source.')


def validate_definition(data, lesson):
    require(isinstance(data, dict) and set(data) <= {'key', 'revision', 'estimated_minutes', 'questions', 'practice_request'}, 'Unknown quiz fields; do not include tools, credentials or schedules.')
    key_revision(data.get('key'), data.get('revision'))
    practical = data.get('practice_request')
    require(practical is None or text(practical), 'practice_request must quote an actual explicit learner training request.')
    minutes = data.get('estimated_minutes')
    require(type(minutes) is int and 1 <= minutes <= (120 if practical else 5), 'Default checks take 1–5 minutes; longer practical checks need an explicit practice_request.')
    questions = data.get('questions')
    require(isinstance(questions, list) and 1 <= len(questions) <= 3, 'Prepare 1–3 lightweight questions per round.')
    ids = []; source_ids = {x['id'] for x in lesson['sources']}; sections = lesson['sections']
    common = {'id', 'kind', 'prompt', 'objective', 'response_hint', 'source_refs', 'hints', 'actions', 'explanation'}
    for q in questions:
        require(isinstance(q, dict), 'Each question must be an object.')
        ids.append(identifier(q.get('id')))
        kind = q.get('kind'); require(kind in ('choice', 'short', 'open'), 'Use choice, short or open questions.')
        extra = {'options', 'answer_id'} if kind == 'choice' else {'expected_answer', 'rubric'}
        require(set(q) == common | extra, 'Question needs only the documented common fields and its type-specific answer fields.')
        require(all(text(q[x]) for x in ('prompt', 'objective', 'response_hint', 'explanation')), 'Question, outcome, response guidance and explanation must be nonempty text.')
        actions = q['actions']
        require(texts(actions) and bool(actions) and len(set(actions)) == len(actions) and set(actions) <= LIGHT | HEAVY, 'Declare the actual required response actions.')
        require(not set(actions) & HEAVY or practical, 'Heavy writing, operations, coding, experiments and projects require an explicit practice_request; otherwise use light questions.')
        require(('select' in actions) == (kind == 'choice'), 'Choice uses selection; text/dialogue questions use brief_text or conversation (or explicitly requested practice).')
        require(texts(q['hints']) and len(q['hints']) <= 3, 'Use up to three short progressive hints.')
        refs = q['source_refs']; require(isinstance(refs, list) and bool(refs), 'Questions need actual lesson source anchors.')
        allowed = set()
        for ref in refs:
            require(isinstance(ref, dict) and set(ref) == {'source_id', 'section_index', 'quote'}, 'Source anchors need source_id, section_index and an exact lesson quote.')
            sid = ref['source_id']; index = ref['section_index']; quote = ref['quote']
            require(isinstance(sid, str) and sid in source_ids and type(index) is int and 0 <= index < len(sections), 'Source/section is outside the selected lesson.')
            require(text(quote) and quote in sections[index]['body'] and f'[{sid}]' in sections[index]['body'], 'Anchor quote and citation must occur in the actual selected lesson section.')
            allowed.add(sid)
        cited_text(q['explanation'], allowed)
        if kind == 'choice':
            options = q['options']; require(isinstance(options, list) and 2 <= len(options) <= 6, 'A single-choice question needs 2–6 options.')
            option_ids = []; option_texts = []
            for option in options:
                require(isinstance(option, dict) and set(option) == {'id', 'text', 'feedback'} and text(option['text']) and text(option['feedback']), 'Options need stable id, displayed text and private feedback.')
                option_ids.append(identifier(option['id'])); option_texts.append(unicodedata.normalize('NFKC', option['text']).strip().casefold())
                cited_text(option['feedback'], allowed)
            require(len(set(option_ids)) == len(options) and len(set(option_texts)) == len(options), 'Option IDs and normalized option texts must be unique.')
            require(isinstance(q['answer_id'], str) and q['answer_id'] in option_ids, 'Answer key must be a canonical option ID, never a display label.')
        else:
            require(text(q['expected_answer']), 'Text questions need private answer guidance.')
            rubric = q['rubric']; require(isinstance(rubric, list) and bool(rubric), 'Text questions need explicit grading criteria.')
            criterion_ids = []
            for item in rubric:
                require(isinstance(item, dict) and set(item) == {'id', 'description'} and text(item['description']), 'Rubric criteria need stable IDs and descriptions.')
                criterion_ids.append(identifier(item['id']))
            require(len(set(criterion_ids)) == len(rubric), 'Rubric IDs must be unique.')
            cited_text(q['expected_answer'], allowed)

    require(len(set(ids)) == len(ids), 'Question IDs must be unique within a revision.')


def validate_feedback(data, question, *, correction=False):
    base = {'strengths', 'gaps', 'explanation', 'source_ids', 'next_step'}
    choice = question['kind'] == 'choice'
    require(isinstance(data, dict) and set(data) == base | ({'verdict'} if choice else {'criteria'}), 'Use documented feedback fields only, without scores or undeclared metadata.')
    require(texts(data['strengths']) and texts(data['gaps']) and text(data['explanation']) and text(data['next_step']), 'Feedback needs explanation, strengths/gaps lists and a small next step.')
    allowed = {x['source_id'] for x in question['source_refs']}
    require(texts(data['source_ids']) and bool(data['source_ids']) and set(data['source_ids']) <= allowed, 'Feedback must cite known question sources.')
    for value in [data['explanation'], data['next_step'], *data['strengths'], *data['gaps']]: cited_text(value, allowed)
    if choice:
        require(correction and data['verdict'] in ('needs_review', 'withdrawn'), 'Disputed choice-key results may be reviewed/withdrawn; use a new quiz revision to change an answer key.')
        return data['verdict']
    criteria = data['criteria']; require(isinstance(criteria, list), 'Feedback criteria must be a list.')
    results = []; ids = []
    for item in criteria:
        require(isinstance(item, dict) and set(item) == {'id', 'result', 'note'} and text(item['note']), 'Criterion feedback needs id, result and note.')
        require(isinstance(item['result'], str) and item['result'] in ('met', 'partly_met', 'not_met', 'uncertain'), 'Unsupported criterion judgment.')
        ids.append(item['id']); results.append(item['result']); cited_text(item['note'], allowed)
    expected = [x['id'] for x in question['rubric']]
    require(all(isinstance(x, str) for x in ids) and len(ids) == len(set(ids)) and set(ids) == set(expected), 'Feedback must cover every frozen rubric criterion exactly once.')
    if 'uncertain' in results: return 'needs_review'
    if all(x == 'met' for x in results): return 'correct'
    if all(x == 'not_met' for x in results): return 'incorrect'
    return 'partial'
