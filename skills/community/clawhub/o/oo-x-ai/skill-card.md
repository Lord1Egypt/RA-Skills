## Description:

xAI (x.ai). Use this skill for ANY xAI request — searching and reading data. Whenever a task involves xAI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with an OOMOL-connected xAI account can use the skill to create chat completions and retrieve model information. It guides the agent to check each action's schema before submitting a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup involves executing a remote CLI installer, and the CLI may synchronize agent skills automatically.

Mitigation: Review and verify a specific CLI release and its synchronization behavior before installation; require user-directed setup.

Risk: Chat completion submits content to OOMOL/xAI and may incur charges.

Mitigation: Treat completion as a user-directed submission, disclose possible charges, and send only content intended for those services to process.

## Reference(s):

- [xAI API Documentation](https://docs.x.ai/)
- [xAI](https://x.ai)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [xAI skill on ClawHub](https://clawhub.ai/oomol/skills/oo-x-ai)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, API response data, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads; connector responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require an authenticated OOMOL account with xAI connected. Chat completion requests can submit content to those services and may incur charges.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
