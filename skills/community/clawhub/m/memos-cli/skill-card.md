## Description:

Use when a user needs to read, search, create, update, delete, comment on, tag, or inspect Memos data through this repository's Go CLI, especially when the agent should prefer real project commands over guessing HTTP API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogeecn](https://clawhub.ai/user/rogeecn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to operate Memos from the terminal through the published Go CLI. It supports reading, searching, creating, updating, deleting, commenting on, tagging, and inspecting Memos data while preferring real CLI commands over hand-written API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run a mutable third-party executable.

Mitigation: Review the upstream memos-cli source and pin a trusted version before installation.

Risk: Memos API credentials and admin credentials may be exposed or overused.

Mitigation: Use HTTPS for non-local servers, keep keys in environment variables or local .env files, never echo secret values, and provide the admin API key only for explicit admin inspection tasks.

Risk: Write and delete commands can modify or remove Memos data.

Mitigation: Run configuration checks first, fetch existing memo content before updates, and require explicit user confirmation before destructive operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogeecn/skills/memos-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/rogeecn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to use --json for machine-readable Memos data and IDs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
