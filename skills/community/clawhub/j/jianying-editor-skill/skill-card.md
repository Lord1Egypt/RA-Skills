## Description:

Jianying Editor Skill helps agents automate JianYing Pro video-editing workflows, including draft generation, media import, subtitles, web-to-video capture, screen recording, and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang21cn-tiger](https://clawhub.ai/user/williamwang21cn-tiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to have an agent assemble JianYing Pro drafts, add media, narration, subtitles, effects, screen recordings, and export-ready timelines from natural-language editing requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent control over JianYing drafts, local media files, GUI export automation, cloud media downloads, and optional screen recording.

Mitigation: Review generated commands and scripts before execution, run the skill in a workspace with only intended media files, and confirm draft and export paths before allowing write or export actions.

Risk: The default intelligent TTS path may send narration text and JianYing device or installation identifiers to a ByteDance endpoint.

Mitigation: Choose a trusted narration backend explicitly before using TTS, and avoid submitting sensitive narration text or identifiers to external services.

Risk: The README includes a shortened PowerShell installer command.

Mitigation: Inspect installer contents or use a manual installation path before running remote PowerShell commands.

Risk: Some export helpers may overwrite existing files when export paths collide.

Mitigation: Use dedicated output directories and check whether target files already exist before running export automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/williamwang21cn-tiger/skills/jianying-editor-skill)
- [README](README.md)
- [Agent Playbook](docs/agent-playbook.md)
- [API Reference](docs/api.md)
- [Minimal Command SOP](docs/minimal-command-sop.md)
- [Available Assets Reference](references/AVAILABLE_ASSETS.md)
- [Bilibili Introduction](https://www.bilibili.com/video/BV1hLzCBzEDS/?vd_source=0eaa8407ec8edd1e9f2a0abf6e126bf6)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or generate local editing scripts and commands that control JianYing drafts, local media, optional screen recording, cloud media downloads, TTS, and export automation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
