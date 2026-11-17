## Description:

Integration with Google Keep via nodriver (undetectable Chrome). Creates, reads, updates, and deletes notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardoreichert](https://clawhub.ai/user/ricardoreichert)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to manage Google Keep notes through command-line browser automation after a one-time Google login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable Google Keep session material on the host.

Mitigation: Use a dedicated Google account or isolated OS user, protect ~/.config/google-keep-skill, and exclude that directory from unsafe backups.

Risk: The skill can headlessly update, delete, archive, or log out of notes and sessions.

Mitigation: Require explicit user confirmation before running update, delete, archive, or logout commands.

Risk: The skill depends on browser automation through nodriver.

Mitigation: Review or pin the nodriver dependency before deployment.

## Reference(s):

- [ClawHub Google Keep Skill page](https://clawhub.ai/ricardoreichert/skills/google-keep-skill)
- [Google Keep](https://keep.google.com/)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI commands return structured JSON for agent interpretation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agents should interpret note data for users instead of exposing raw JSON.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter 1.0.0 and pyproject.toml 0.3.0 differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
