## Description:

Recall.ai (recall.ai). Use this skill for ANY Recall.ai request — reading, creating, updating, and deleting data. Whenever a task involves Recall.ai, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and meeting automation users use this skill to inspect Recall.ai bots, create meeting bots, and manage active bots or completed media through an OOMOL-connected Recall.ai account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute changing remote code and introduce broader agent-skill changes; the remote installers and hosted connector implementation were not verified.

Mitigation: Review CLI installation separately and use a verified release. Before running it, consider setting OO_SKILLS_SYNC_DISABLED=1 to prevent automatic agent-skill changes.

Risk: Connecting Recall.ai authorizes OOMOL to handle Recall.ai requests and credentials.

Mitigation: Connect only the intended Recall.ai account and review its authorization before using the skill.

Risk: Creating bots, removing a bot from a call, or deleting bot media changes or removes data.

Mitigation: Inspect the live action schema, then confirm the exact payload and effect with the user before write or destructive actions.

## Reference(s):

- [Recall.ai API documentation](https://docs.recall.ai/)
- [Recall.ai](https://www.recall.ai)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions]

**Output Format:** [JSON command payloads and API responses, with Markdown guidance and inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads follow the live connector schema; responses include data and an execution ID.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
