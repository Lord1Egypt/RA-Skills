## Description:

A general-purpose skill for connecting the organization platform with external agents. Use it to access user, organization, post, and activity APIs, and to complete authentication, organization operations, content publishing, and activity workflows whenever an agent needs to execute actions through the platform APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urzeye](https://clawhub.ai/user/urzeye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate ZingUp and Groupoo organization workflows through a bundled CLI, including authentication, organization management, post publishing, and activity draft, publish, search, and signup flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run authenticated actions against real ZingUp and Groupoo accounts, including production organization, post, and activity operations.

Mitigation: Review commands before execution and use test mode for development or integration testing.

Risk: Session files can contain access tokens, refresh tokens, and device identifiers.

Mitigation: Store session files outside shared repositories, protect or rotate tokens, and avoid logging authentication responses.

Risk: Untrusted prompts or configuration could redirect authenticated requests through --base-url or ORG_SKILL_BASE_URL.

Mitigation: Do not allow untrusted input to set base URLs for authenticated commands.

Risk: Some actions, such as bans, disputes, credit penalties, or offline safety decisions, can carry high operational impact.

Mitigation: Keep human fallback and review for high-risk organization operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urzeye/skills/organization-operating-skill)
- [Organization Operating Skill README](README.md)
- [Auth & Environment Reference](references/auth_reference.md)
- [Org Reference](references/org_reference.md)
- [Content Reference](references/content_reference.md)
- [Activity Reference](references/activity_reference.md)
- [API Reference Index](references/api_reference.md)
- [Capability Inventory](references/capability_inventory.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may execute HTTP API calls and write local session JSON outside the skill repository.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
