"""Validate a host-authored study brief; semantic analysis stays with the agent."""


def text(value):
    return isinstance(value, str) and bool(value.strip())


def texts(value, nonempty=False):
    return isinstance(value, list) and (bool(value) or not nonempty) and all(text(x) for x in value)


def validate_brief(value):
    fields = {'request', 'interpretation', 'outcomes', 'scope', 'prerequisites',
              'sequence', 'assumptions', 'open_questions'}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError('learning_brief needs request, interpretation, outcomes, scope, prerequisites, sequence, assumptions and open_questions.')
    if not text(value['request']) or not text(value['interpretation']) or not texts(value['outcomes'], True):
        raise ValueError('Brief needs the original study request, interpretation and nonempty outcomes.')
    scope = value['scope']
    if not isinstance(scope, dict) or set(scope) != {'included', 'excluded'} or not texts(scope['included'], True) or not texts(scope['excluded']):
        raise ValueError('Brief scope needs nonempty included topics and an excluded list (which may be empty).')
    if not texts(value['prerequisites']) or not texts(value['open_questions']):
        raise ValueError('Brief prerequisites and open_questions must be text lists; empty lists are valid.')
    sequence = value['sequence']
    if not isinstance(sequence, list) or not sequence or any(
        not isinstance(x, dict) or set(x) != {'topic', 'outcome'} or not text(x['topic']) or not text(x['outcome']) for x in sequence
    ):
        raise ValueError('Brief sequence needs ordered topic/outcome records.')
    assumptions = value['assumptions']
    if not isinstance(assumptions, list) or any(
        not isinstance(x, dict) or set(x) != {'statement', 'status'} or not text(x['statement']) or x['status'] not in ('proposed', 'confirmed') for x in assumptions
    ):
        raise ValueError('Brief assumptions need statement and proposed/confirmed status.')
    return {'valid': True, 'needs_confirmation': bool(value['open_questions']) or any(x['status'] == 'proposed' for x in assumptions),
            'note': 'Structure check only; the host must verify topic fit, research, learner consent and teaching quality.'}
