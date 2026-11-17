## Description:

Personal AI (personal.ai). Use this skill for ANY Personal AI request — reading, creating, and updating data. Whenever a task involves Personal AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Personal AI users use this agent to read, create, and update Personal AI data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup asks the user to run a remote installer that was not inspected; its local changes are uncertain.

Mitigation: Review the fallback installation before enabling it, or preinstall a reviewed, version-pinned CLI.

Risk: Messages, instructions, and uploaded content can change or add data in the connected Personal AI account.

Mitigation: Approve the exact message or document before each write.

## Reference(s):

- [Personal AI homepage](https://personal.ai)
- [Personal AI API documentation](https://docs.personal.ai/api-reference/endpoint/ai-message)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Guidance]

**Output Format:** [Shell commands with JSON request payloads; JSON responses and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
