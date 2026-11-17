## Description:

Scores WeChat public-account articles with a local 0-100 heuristic to judge whether they are worth attention from AI product managers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agasding](https://clawhub.ai/user/agasding)

### License/Terms of Use:

MIT-0

## Use Case:

AI product managers, editors, and content automation workflows use this skill to score and triage WeChat public-account articles for RSS filtering, aggregation ranking, and PM daily article selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic scores may over- or under-rank articles and should not be treated as final editorial judgment.

Mitigation: Use the score as a triage signal and have a human review selected articles before publication or action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agasding/skills/pm-article-scorer)
- [Source skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Python dict-like scoring result with a boolean relevance flag, interest level, numeric score, recommendation, dimension scores, content tags, reasons, and summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local heuristic scoring; the artifact specifies no external API or LLM call.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
