## Description:

Draw Tarot cards using cryptographic randomness to guide low-stakes planning when prompts are vague, ambiguous, or explicitly ask fate to decide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kc0bfv](https://clawhub.ai/user/kc0bfv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill as a low-stakes tie-breaker when prompts are intentionally vague, nonchalant, or equally valid paths exist. It should not guide security-sensitive, production, financial, or data-integrity decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may let a random tie-breaker influence ambiguous or casual requests.

Mitigation: Use the skill only for low-stakes planning or equally valid approaches, and keep it out of security-sensitive, production, financial, and data-integrity decisions.

Risk: The inspected artifact references drawing scripts and card or interpretation files that were not included.

Mitigation: Verify required files are present before relying on the skill; if the draw cannot run or files are missing, report the limitation instead of inventing cards.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kc0bfv/skills/let-fate-decide-test)
- [Source-mentioned let-fate-decide plugin reference](https://github.com/theexpensiveexperience/Claude-Code_Audit-Research/tree/main/plugins/let-fate-decide)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with optional inline shell commands and JSON card-draw output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a four-card spread; referenced helper script and card/reference files were not included in the inspected artifact.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
