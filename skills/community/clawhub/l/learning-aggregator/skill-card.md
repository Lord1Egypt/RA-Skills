## Description:

[Beta] Cross-session analysis of accumulated .learnings/ files. Reads all entries, groups by pattern_key, computes recurrence across sessions, and outputs ranked promotion candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pskoett](https://clawhub.ai/user/pskoett)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect accumulated local learning files, identify recurring gaps across sessions, and prioritize promotion candidates for instructions, tools, skills, or evaluations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional deep mode can read full historical session transcripts, which may include secrets or unrelated private work.

Mitigation: Use deep analysis only after confirming the selected checkpoints are relevant, and review generated gap reports before sharing or committing them.

Risk: Gap reports may contain incorrect or over-broad promotion recommendations for ambiguous patterns.

Mitigation: Require human review before applying recommendations to project instructions, skills, tools, or evaluations.

## Reference(s):

- [Learning Aggregator skill page](https://clawhub.ai/pskoett/skills/learning-aggregator)
- [Entire](https://entire.io)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance, shell commands]

**Output Format:** [Markdown gap report with ranked pattern summaries, evidence, recommended actions, and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include filters by date, area, recurrence threshold, and optional deep trace analysis when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
