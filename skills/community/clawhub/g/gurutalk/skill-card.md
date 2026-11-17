## Description:

GuruTalk manages local digital persona directories by syncing Bibliotalk profiles, generating persona skill folders, and routing ongoing conversations to selected figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casterkay](https://clawhub.ai/user/casterkay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install, sync, list, remove, and version local persona skills backed by Bibliotalk profiles. Generated personas can answer with cited source material after the user starts a figure-specific conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write and delete local skill folders.

Mitigation: Review requested create, sync, remove, snapshot, and rollback operations before execution, and run them only for trusted figure slugs and expected agent directories.

Risk: The skill stores a Bibliotalk API key locally and may copy runtime configuration into generated persona skills.

Mitigation: Use only a Bibliotalk account and API key suitable for local storage, avoid pasting secrets into chat, and rotate the key if generated skill folders are shared or exposed.

Risk: Generated personas can introduce incorrect or misleading profile content or advice.

Mitigation: Review generated persona profiles and require cited Bibliotalk evidence for substantive claims; treat uncited or insufficiently supported answers as unreliable.

## Reference(s):

- [GuruTalk ClawHub release page](https://clawhub.ai/casterkay/skills/gurutalk)
- [Bibliotalk](https://bibliotalk.space)
- [Bibliotalk API endpoint](https://api.bibliotalk.space)
- [AgentSkills standard](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown text with inline shell commands and generated local skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, sync, remove, snapshot, and roll back local persona skill folders for Claude Code, Codex, and OpenClaw.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
