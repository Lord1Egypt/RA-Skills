## Description:

My Study Pal is a Chinese study assistant that explains unfamiliar concepts, terms, abbreviations, and distinctions for adult learners while maintaining local study records and learner profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanyqw](https://clawhub.ai/user/ivanyqw)

### License/Terms of Use:

MIT-0

## Use Case:

External learners use this skill to get concise Chinese explanations of unfamiliar concepts, abbreviations, terms, and differences, with optional guided, applied, contrastive, and retention-oriented teaching modes. The skill also records study progress and preferences in local workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically saves study topics, preferences, profile details, and full conversation records in local mystudy files by default.

Mitigation: Use it only in workspaces where this storage is acceptable, avoid sensitive topics, and review or clean the mystudy folder regularly.

Risk: Local study records may include personal learning context or confidential details if users discuss them during concept explanations.

Mitigation: Do not use it with secrets, confidential work details, health information, financial information, or anything that should not be stored locally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivanyqw/skills/my-study-pal)
- [Setup - my-study-pal](setup.md)
- [Filesystem Blueprint - my-study-pal](references/blueprint.md)
- [Concept Explanation Storage Specification](references/study-storage.md)
- [Recording Rules](references/recording-rules.md)
- [Response Contract](references/response-contract.md)
- [Direct Answer Mode](references/method-direct.md)
- [Expository Teaching Method](references/method-expository.md)
- [Guided Questioning Method](references/method-guided.md)
- [Contrastive Teaching Method](references/method-contrastive.md)
- [Applied Teaching Method](references/method-applied.md)
- [Retention Teaching Method](references/method-retention.md)
- [Style Analysis Framework](references/style-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown explanations with optional shell commands and local Markdown study record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update mystudy/study-summary.md, mystudy/user-profile.md, mystudy/runtime-profile.md, and mystudy/study-detail/*.md in the active workspace.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
