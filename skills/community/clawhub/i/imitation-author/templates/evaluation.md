# Evaluation For {{target}}

## Run Metadata

- Date:
- Generated skill version/hash:
- Authorization mode:
- Evaluator: `fresh AI/model/person | authoring AI`
- Evaluation status: `independent | provisional self-evaluation`
- Prompt set frozen before review: `yes | no`

## Corpus Split

### Inference Set

- Corpus IDs:
- Channels/topics/periods:

### Held-Out Evaluation Set

- Corpus IDs:
- Channels/topics/periods:
- Contamination risk:

### Counter-Corpus

- Corpus IDs:
- Why these control for topic or genre:

## Test Prompts

| Test | Prompt | Mode | What it tests |
|---|---|---|---|
| Requested topic | {{requested_topic}} |  | Near-domain usefulness and fidelity |
| Cross-topic |  |  | Style beyond topic vocabulary |
| Cross-mode |  |  | Claimed channel portability |

## Candidates

### Skill-Guided Candidate

...

### Negative Control

Write a competent generic answer to the same brief without the target skill.

...

## Topic And Genre Controls

- Topic words/proper nouns ignored during style judgment:
- Shared genre conventions not credited as target-specific:
- Counter-corpus comparison:
- Does the target signal survive the cross-topic test?

## Phrase-Overlap Check

- Method: exact sequences of six or more words | strongest manual alternative
- Corpus searched:
- Matches reviewed:
- Distinctive or suspicious matches:
- Revisions:
- Limitation:

## Independent Evaluation

Randomize candidate order. Provide prompt, Claim-ID rubric, and lawful held-out observations. Do not reveal which draft used the skill.

| Dimension | Skill candidate (1-5) | Negative control (1-5) | Evidence and Claim IDs |
|---|---:|---:|---|
| content quality |  |  |  |
| selection style fidelity |  |  |  |
| reasoning style fidelity |  |  |  |
| composition style fidelity |  |  |  |
| linguistic style fidelity |  |  |  |
| naturalness |  |  |  |
| originality |  |  |  |
| authorization/safety | pass/fail | pass/fail |  |
| portability to a fresh AI | pass/fail | not applicable |  |

## Held-Out Comparison

| Claim ID | Candidate behavior | Held-out confirmation, complication, or contradiction | Result |
|---|---|---|---|
|  |  |  | pass/partial/fail |

## Anti-Caricature Review

| Surface feature | Observed frequency | Allowed calibration | Result |
|---|---:|---|---|
|  |  |  | pass/overused/missing |

## Gate

- Content quality and naturalness at least 4/5:
- Mean style fidelity at least 4/5, no component below 3:
- Skill candidate beats Negative Control by at least one mean fidelity point:
- No worse than control on content quality or naturalness:
- Phrase-overlap check clean:
- Authorization/safety pass:
- Fresh-AI portability pass:
- Result: `pass | revise skill | revise sample | research insufficient`

## Verdict

- What clearly reflects supported target traits:
- What remains generic:
- What feels exaggerated or copied:
- Which Claim IDs were missed or overused:
- Narrowest defensible conclusion:
- Next revision:
