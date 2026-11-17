## Description:

Manage Obsidian vaults via LiveSync CouchDB: capture notes, AI-enrich and file them, manage tasks, audit, and tidy vault structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philmossman](https://clawhub.ai/user/philmossman)

### License/Terms of Use:

MIT

## Use Case:

Developers and Obsidian users use this skill to manage an Obsidian vault through the CouchDB database used by Obsidian LiveSync, including note capture, inbox processing, filing, auditing, tidying, and task management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm CLI receives plaintext read/write access to a LiveSync CouchDB vault that may contain sensitive notes.

Mitigation: Install only after reviewing the package and configure it for vaults where this level of access is acceptable.

Risk: Cloud AI provider behavior is under-disclosed for note content processed by AI features.

Mitigation: Use the local or none AI provider for sensitive vaults unless documentation clearly states what content is sent to cloud providers.

Risk: The install metadata does not pin the npm package version.

Mitigation: Prefer a pinned, reviewed package version for deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philmossman/skills/obsidian-curator)
- [Publisher profile](https://clawhub.ai/user/philmossman)
- [obsidian-curator npm package](https://www.npmjs.com/package/obsidian-curator)
- [obsidian-curator GitHub repository](https://github.com/philmossman/obsidian-curator)
- [Obsidian LiveSync](https://github.com/vrtmrz/obsidian-livesync)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands, JavaScript examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dry-run commands before vault-changing operations.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
