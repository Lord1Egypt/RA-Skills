## Description:

Shared web task memory for AI agents that helps agents query community workflow knowledge before browsing and report execution traces after tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yourens](https://clawhub.ai/user/yourens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use NaviMem to plan browser automation tasks with shared workflow memory, query for page actions when stuck, and report sanitized task traces after completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser task descriptions and workflow traces may be sent to a third-party service with incomplete privacy controls.

Mitigation: Use the skill only for non-sensitive public web automation and avoid authenticated accounts, credentials, private URLs, personal data, payments, health, finance, and internal business systems.

Risk: Shared workflow plans may be outdated or not match the live page state.

Mitigation: Treat returned plans as guidance and verify each suggested action against the current page before executing it.

## Reference(s):

- [ClawHub NaviMem release](https://clawhub.ai/yourens/skills/navimem)
- [NaviMem API base URL](https://i.ariseos.com)
- [Plan endpoint](https://i.ariseos.com/api/v1/memory/plan)
- [Query endpoint](https://i.ariseos.com/api/v1/memory/query)
- [Learn endpoint](https://i.ariseos.com/api/v1/memory/learn)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require NAVIMEM_BASE_URL to override the default NaviMem API base URL.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
