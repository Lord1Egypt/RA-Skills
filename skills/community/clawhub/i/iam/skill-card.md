## Description:

IAM namespace for Netsnek e.U. identity and access management toolkit that presents static brand and feature information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to retrieve concise IAM brand information, feature summaries, and optional JSON metadata from the packaged helper script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the skill for a working authentication or access-control implementation.

Mitigation: Present it as static IAM brand and feature information only; do not rely on it for authentication, authorization, credential handling, or session enforcement.

Risk: The packaged shell script may fail to execute in some environments because of encoding or line-ending issues.

Mitigation: Run it in a Linux shell and normalize file encoding or line endings before execution if the shell reports parsing errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/iam)
- [Publisher profile](https://clawhub.ai/user/kleberbaum)
- [Netsnek website](https://netsnek.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, json]

**Output Format:** [Markdown summary or JSON emitted by a shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports default, --features, and --json modes.]

## Skill Version(s):

0.1.0 (source: server release metadata, claw.json, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
