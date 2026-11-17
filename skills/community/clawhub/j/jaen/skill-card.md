## Description:

Jaen provides copyright and brand identity information for the Netsnek e.U. Jaen CMS framework namespace on ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to retrieve Jaen and Netsnek e.U. brand identity, copyright notice, website information, and optional JSON-formatted copyright output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests exec permission for a local script.

Mitigation: Review the packaged script before granting exec permission and limit use to the observed copyright and website information behavior.

Risk: The artifact uses broad trigger and response wording for Jaen brand questions.

Mitigation: Invoke it only for Jaen or Netsnek e.U. identity and copyright requests, and treat the script output as brand information rather than general CMS guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/jaen)
- [Netsnek website](https://netsnek.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON, typically summarized by the agent in a concise user-facing response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires exec permission to run scripts/copyright.sh; supports --format text and --format json.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, claw.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
