## Description: <br>
Provides a Python wrapper and agent workflow for automating JianYing Pro video drafts, including media import, subtitles, screen recording, web-to-video effects, text-to-speech, and export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwang21cn-tiger](https://clawhub.ai/user/williamwang21cn-tiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and video automation agents use this skill to generate and edit JianYing Pro drafts from local or cloud media, add narration, subtitles, effects, and export videos through scripted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A one-line PowerShell installer may obscure what code is downloaded or executed. <br>
Mitigation: Prefer an inspectable, pinned release or repository checkout before installation. <br>
Risk: Screen recording, local draft inspection, transcript handling, cloud media, and TTS workflows can expose sensitive video, desktop, credential, or private speech content. <br>
Mitigation: Use test projects first, avoid sensitive inputs unless the data-handling path is approved, and review any external AI or TTS services before use. <br>
Risk: Automated UI and file operations can change JianYing drafts, cache files, logs, or export outputs. <br>
Mitigation: Keep backups, run on disposable drafts initially, and verify generated project structure before using production media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamwang21cn-tiger/jianying-editor-skill) <br>
- [Agent Playbook](docs/agent-playbook.md) <br>
- [API Reference](docs/api.md) <br>
- [Minimal Command SOP](docs/minimal-command-sop.md) <br>
- [Available Assets Reference](references/AVAILABLE_ASSETS.md) <br>
- [JianYing Reference README](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets, plus generated Python scripts and JSON CLI output when used by an agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create JianYing draft files, media exports, subtitles, and local recordings when executed in a configured environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
