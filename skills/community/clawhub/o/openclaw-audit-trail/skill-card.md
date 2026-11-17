## Description:

Track, audit, and verify AI agent decisions with cryptographic guarantees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add local audit logging for AI agent decisions, verify hash-chain integrity, and export audit records for compliance review, incident analysis, and debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable audit logs and exports may contain prompts, context, reasoning, personal data, secrets, or regulated data.

Mitigation: Redact sensitive fields before recording, restrict access to audit storage and exports, apply retention limits, and treat generated audit artifacts as confidential.

Risk: External installation paths may resolve to unreviewed package contents if versions or commits are not pinned.

Mitigation: Install only pinned, reviewed versions or commits in a contained environment before using the skill with production data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/openclaw-audit-trail)
- [Publisher Profile](https://clawhub.ai/user/zhenstaff)
- [Homepage](https://github.com/ZhenRobotics/openclaw-audit-trail)
- [NPM Package](https://www.npmjs.com/package/openclaw-audit-trail)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
