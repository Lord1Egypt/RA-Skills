## Description:

Helps an agent read, search, create, and update notes in a user-owned Obsidian vault through the Local REST API plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nj070574-gif](https://clawhub.ai/user/nj070574-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Obsidian users and their agents use this skill to find, read, organize, and update notes in the user's configured vault on Windows, macOS, or Linux.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reusable API key grants broad access to the user's vault.

Mitigation: Keep the key secret, limit installation to a vault you own, and rotate the key if exposed.

Risk: Unverified TLS could expose the API key and note contents.

Mitigation: Use the plugin certificate via OBSIDIAN_CA_CERT or a CA-trusted reverse proxy; avoid the TLS bypass.

Risk: Overwriting or deleting a note can remove existing content.

Mitigation: Confirm the exact target and intended change with the user before destructive actions.

Risk: Instructions embedded in retrieved notes could redirect the agent.

Mitigation: Treat note content as data, not instructions to execute.

## Reference(s):

- [Obsidian Local REST API plugin](https://github.com/coddingtonbear/obsidian-local-rest-api)
- [Obsidian Local REST API skill on ClawHub](https://clawhub.ai/nj070574-gif/skills/obsidian-rest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Concise prose and Markdown, with shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return note contents or summarize vault search results and changes.]

## Skill Version(s):

1.3.0 (source: server-resolved release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
