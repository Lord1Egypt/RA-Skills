## Description: <br>
Control a remote Obsidian vault through Fast Note Sync. Use when reading, searching, writing, or appending notes in Obsidian from OpenClaw, especially for remote vault workflows that do not have direct filesystem access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[attack-flower](https://clawhub.ai/user/attack-flower) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search, read, write, append, and manage notes in a remote Obsidian vault through a configured Fast Note Sync endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent persistent authority to read and mutate a remote Obsidian vault. <br>
Mitigation: Install only for trusted Fast Note Sync endpoints and require explicit path and content confirmation before replace, rename, move, overwrite, or restore-history operations. <br>
Risk: Passwords or tokens may be stored in plaintext local configuration. <br>
Mitigation: Prefer environment variables or a secure secret store over set-config for credentials, passwords, or tokens. <br>
Risk: Login output or command logs can expose authentication tokens. <br>
Mitigation: Avoid printing or retaining login output in shared logs and rotate tokens if they are exposed. <br>


## Reference(s): <br>
- [Obsidian FNS ClawHub page](https://clawhub.ai/attack-flower/obsidian-fns) <br>
- [obsidian-fns usage reference](artifact/references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text or JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates against the configured Fast Note Sync endpoint and may read or modify remote Obsidian vault content.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
