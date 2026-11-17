## Description:

Nora Persona Framework guides users through creating local AI persona files with preset or custom dual-mode styles, voice settings, and persona consistency reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallyface0](https://clawhub.ai/user/sallyface0)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and refine local AI companion personas. It can generate SOUL.md, IDENTITY.md, AGENTS.md, and optional persona consistency reports after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent persona files can steer future agent sessions and may include broad obedience, priority override, or identity-hiding rules.

Mitigation: Review generated SOUL.md, IDENTITY.md, and AGENTS.md before approval; reject rules that override normal instruction priority or conceal assistant identity.

Risk: Persona files, backups, and watchdog reports may preserve personal preferences or conversation-derived details in the workspace.

Mitigation: Keep persona content non-sensitive, approve writes only after preview, and delete SOUL.md, IDENTITY.md, AGENTS.md, SOUL.md.bak, or memory/persona-check-*.md when no longer needed.

Risk: Voiceclone configuration can reference user-provided audio or paths that may reveal personal information.

Mitigation: Use non-sensitive reference audio and paths, and keep voiceclone references local unless the user separately chooses to share them.

## Reference(s):

- [Nora Persona Framework on ClawHub](https://clawhub.ai/sallyface0/skills/nora-persona-framework)
- [README.md](artifact/README.md)
- [PRIVACY.md](artifact/PRIVACY.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and local workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local persona, identity, agent guidance, backup, and persona-check report files only after user confirmation.]

## Skill Version(s):

1.4.1 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
