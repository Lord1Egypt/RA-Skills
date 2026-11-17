## Description:

Controls the LX Music desktop app for music search, playback, playlists, volume, favorites, status, and lyrics, then reports command results in Markdown tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ly14sh](https://clawhub.ai/user/ly14sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent control a local LX Music desktop client, search and play music, inspect status or lyrics, manage favorites, and query or play local playlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled playlist code has a shell-command-injection risk when invoking Python with playlist IDs or custom database paths.

Mitigation: Fix the CLI to use non-shell process execution and pass playlist IDs and database paths as argument arrays before broad use.

Risk: Installing the skill grants a local assistant control over LX Music playback, favorites, lyrics and status reads, and local playlist database access.

Mitigation: Install only in trusted local environments and avoid passing untrusted playlist IDs or custom database paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ly14sh/skills/lx-music-assistant)
- [LX Music CLI commands reference](artifact/references/commands.md)
- [LX Music OpenAPI service](artifact/references/open-api.md)
- [LX Music Scheme URL support](artifact/references/scheme-url.md)
- [LX Music OpenAPI documentation](https://lxmusic.toside.cn/desktop/open-api)
- [LX Music Scheme URL documentation](https://lxmusic.toside.cn/desktop/scheme-url)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables with inline command results and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured LX Music OpenAPI endpoint and may read the local LX Music playlist database.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
