## Description:

Organize mission and agent memory with explicit scope, provenance, retention, access controls, and deletion rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdjahid11978-design](https://clawhub.ai/user/mdjahid11978-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent designers use this skill to organize working, session, project, and agent memory with provenance, access, retention, correction, and deletion controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memory may include sensitive information or persist beyond its purpose.

Mitigation: Avoid secrets and unnecessary sensitive data; use least-privilege access and set purpose-based retention and expiry.

Risk: Remembered instructions could be mistaken for current authorization.

Mitigation: Treat memory as context only and follow current policy and consent; support correction and deletion of memory.

## Reference(s):

- [Server-resolved source repository](https://github.com/mdjahid11978-design/Jahids-skills/tree/main/skills/jahids-memory-manager)
- [ClawHub release page](https://clawhub.ai/mdjahid11978-design/skills/jahids-memory-manager)

## Skill Output:

**Output Type(s):** [Guidance, Configuration]

**Output Format:** [Structured text describing a scoped memory operation and its provenance and retention metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
