## Description:

Migrate, back up, or restore an OpenClaw agent workspace to or from a single .soul archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagura-agent](https://clawhub.ai/user/kagura-agent)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw operators use this skill to move an agent workspace to a new machine, create backups, restore from a .soul archive, or clone an agent setup. It is intended for full workspace migration workflows that may include identity files, memory, configuration, credentials, cron jobs, repositories, and services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: .soul archives can contain plaintext credentials such as API tokens, bot tokens, app secrets, and channel credentials.

Mitigation: Treat .soul files like password files: keep them out of git and public cloud sync, transfer them through encrypted channels, and encrypt backups before storage or transfer.

Risk: Restoring an archive can write configuration and credentials, restore cron jobs, clone repositories, install OpenClaw if missing, and start services.

Mitigation: Inspect archives before unpacking, restore only archives from trusted sources, and prefer an isolated account or sandbox when evaluating a package version.

Risk: The server security verdict is suspicious because the skill handles plaintext credentials and restores scheduled jobs or services through mutable npm code.

Mitigation: Review the package and archive contents before installation or restore, and use a pinned, verified package version when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kagura-agent/skills/openclaw-teleport)
- [Publisher profile](https://clawhub.ai/user/kagura-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers pack, unpack, inspect, and security handling for .soul archives.]

## Skill Version(s):

0.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
