## Description:

Diagnose and fix openclaw gateway issues. Use when the gateway is stuck, not starting, crash-looping, or rejecting connections. Covers main and --profile vesper gateways. Runs triage, applies fixes, writes incident report to ~/clawd/inbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siraustin](https://clawhub.ai/user/siraustin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to triage, repair, and document OpenClaw gateway failures across the main and vesper profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway tokens or setup-token files could be exposed in chat or logs during troubleshooting.

Mitigation: Run only in a trusted OpenClaw operations context and prevent agents from printing tokens or reading setup-token files into shared outputs.

Risk: The skill can guide persistent changes to configs, plists, session files, lock files, and LaunchAgents.

Mitigation: Require explicit approval and backups before applying edits, deleting files, pruning sessions, or restarting LaunchAgents.

## Reference(s):

- [OpenClaw DX release page](https://clawhub.ai/siraustin/skills/openclaw-dx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local config, plist, session, lock-file, and LaunchAgent changes; incident reports are written as Markdown.]

## Skill Version(s):

1.9.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
