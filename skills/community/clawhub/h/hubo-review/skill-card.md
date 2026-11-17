## Description:

Reviews without editing, then has a critic challenge every finding and missed risk until the review is reconciled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h0ngcha0](https://clawhub.ai/user/h0ngcha0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Hubo Review to run a read-only review of code, diffs, pull requests, tests, designs, or technical claims, with a critic challenging findings and omissions until the review is reconciled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The multi-agent critic loop can increase runtime or usage cost.

Mitigation: Use the skill when critical review depth justifies multiple agent sessions, and stop when the critic returns CLEAR or a user decision is required.

Risk: A host that cannot mechanically block mutation tools may make the read-only boundary harder to verify.

Mitigation: Block mutation tools when possible, compare before-and-after evidence around role turns, and report when the boundary cannot be verified.

## Reference(s):

- [Hubo Review on ClawHub](https://clawhub.ai/h0ngcha0/skills/hubo-review)
- [Karpathy-inspired discipline](https://github.com/multica-ai/andrej-karpathy-skills)
- [Ponytail](https://github.com/DietrichGebert/ponytail)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report and chronological reviewer/critic transcript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only review output mirrored into the conversation; no files are written by the skill.]

## Skill Version(s):

0.4.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
