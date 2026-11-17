## Description:

Crisp (crisp.chat). Use this skill for ANY Crisp request — reading, creating, and updating data. Whenever a task involves Crisp, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support teams use this skill to retrieve Crisp website and conversation details, list messages and conversations, and send operator text messages through a connected Crisp account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may install persistent agent skills without this skill describing the full installation effect.

Mitigation: Review CLI installation separately; set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI to prevent startup skill writes, and keep confirmation enabled for outgoing messages.

## Reference(s):

- [Crisp API documentation](https://docs.crisp.chat/references/rest-api/v1/)
- [Crisp](https://crisp.chat/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands, JSON action responses, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can retrieve conversation and website data or send operator text messages.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
