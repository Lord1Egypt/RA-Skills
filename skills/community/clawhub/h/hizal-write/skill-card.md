## Description:

Hizal Write guides an agent to persist useful learnings, decisions, conventions, identity notes, organization knowledge, and principles through dedicated Hizal write tools during work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkerscobey](https://clawhub.ai/user/parkerscobey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to record decisions, lessons, project conventions, organization knowledge, and related memory while work is happening so future sessions can reuse that context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory writes can store sensitive or unverified information if scopes and content are not controlled.

Mitigation: Constrain approved scopes, require confirmation for project or organization writes, and avoid storing secrets, credentials, personal data, raw conversation content, or unverified claims.

Risk: Auto-injected memory or identity entries can influence future agent behavior without clear user control.

Mitigation: Use auto-injection only for deliberately approved memory categories and review durable identity or convention writes before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkerscobey/skills/hizal-write)

## Skill Output:

**Output Type(s):** [Guidance, Text, Code]

**Output Format:** [Markdown with inline tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for durable memory writes across agent, project, and organization scopes.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
