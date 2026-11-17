## Description:

Adaptive token-conservation system that helps an agent reduce narration, formatting, and process detail across low, medium, and extreme token-saving modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make agent responses and workflows more concise when token budgets, quotas, or rate limits require conservation. It is intended to preserve accuracy and safety checks while reducing nonessential narration and formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reduce confirmations and visibility before actions are taken.

Mitigation: Review before installation and rely on separate safety rules for risky, destructive, or externally visible actions.

Risk: Higher conservation modes may omit detailed summaries that some workflows depend on.

Mitigation: Use LOW mode for normal operation and reserve MEDIUM or EXTREME mode for constrained token budgets, quota pressure, or explicit user requests.

## Reference(s):

- [Low Token Usage Skill Page](https://clawhub.ai/tooled-app/skills/low-token)
- [Demystify](https://demystify.website)
- [IKKF](https://ikkf.info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise natural-language guidance, compact summaries, and minimal command-oriented responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Three conservation levels: LOW, MEDIUM, and EXTREME. Output may omit confirmations, detailed summaries, and markdown decoration in higher conservation modes.]

## Skill Version(s):

2.1.0 (source: server release metadata and SKILL.md title)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
