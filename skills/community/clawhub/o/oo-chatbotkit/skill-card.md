## Description:

Use this skill for any ChatBotKit request, including reading, creating, updating, or deleting data, instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to manage ChatBotKit bots, conversations, datasets, files, and usage through an OOMOL-connected account. It guides the agent to inspect each action schema and use the oo CLI to run the corresponding request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup runs remote installer code whose exact contents and delivered release are unverified.

Mitigation: Before installing, inspect and verify the distribution and confirm which release it will deliver.

Risk: Startup synchronization can make broader changes to agent skills without disclosing them.

Mitigation: Review whether broader skill installation is acceptable; use OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization if needed.

Risk: Writes and deletions affect ChatBotKit account data through the connected OOMOL account.

Mitigation: Inspect the action schema and confirm the exact payload and effect before writes; explicitly approve the target before destructive actions.

## Reference(s):

- [ChatBotKit](https://chatbotkit.com)
- [ChatBotKit API documentation](https://chatbotkit.com/docs/api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON service responses and Markdown guidance with oo CLI shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas should be inspected before requests; writes and destructive actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
