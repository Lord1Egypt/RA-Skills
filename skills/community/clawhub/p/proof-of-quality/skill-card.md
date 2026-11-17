## Description:

Generates a Bitcoin-style proof-of-work quality proof for a skill when its benchmark score exceeds a threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kunoiiv](https://clawhub.ai/user/kunoiiv)

### License/Terms of Use:


## Use Case:

Developers and skill reviewers use this skill to run a local proof-of-work script that reports a score, hash, and nonce for a target skill. Its output should be treated as advisory and not as a standalone approval gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proof-of-quality result can be mistaken for a trustworthy quality or security gate.

Mitigation: Use the PoQ output only as advisory signal and require independent review, testing, and security assessment before approving skills, forks, or collaborators.

Risk: Recurring cron execution can create unnecessary CPU work.

Mitigation: Avoid scheduling recurring runs unless target paths, frequency, runtime limits, and CPU limits are explicitly defined.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kunoiiv/skills/proof-of-quality)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown guidance and console text; proof data includes score, hash, and nonce.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against a skill path and numeric threshold.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
