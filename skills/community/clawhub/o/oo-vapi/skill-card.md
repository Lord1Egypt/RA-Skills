## Description:

Vapi (vapi.ai). Use this skill for ANY Vapi request — reading, creating, updating, and deleting data. Whenever a task involves Vapi, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Vapi resources through an OOMOL-connected account, including retrieving data and creating, updating, or deleting assistants, calls, chats, phone numbers, and related resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded CLI code that has not been verified, and automatic skill synchronization may affect the local environment.

Mitigation: Review and verify the CLI installer before installation, and control automatic skill synchronization.

Risk: The code-execution action runs TypeScript in Vapi's sandbox; its behavior should not be treated as read-only.

Mitigation: Require review and approval of the exact code and its expected effects before using the code-execution action.

## Reference(s):

- [Vapi API Reference](https://docs.vapi.ai/api-reference)
- [Vapi](https://vapi.ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-vapi)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [Structured JSON results with concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Vapi action and connected account.]

## Skill Version(s):

1.0.7 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
