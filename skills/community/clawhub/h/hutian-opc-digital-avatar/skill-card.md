## Description: <br>
Guides agents through configuring OPC-focused digital avatar videos across appearance, voice, language style, background, duration, and target generation platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, OPC operators, and developers use this skill to plan digital-human videos by selecting persona templates, voice settings, language style, backgrounds, durations, and platform-specific output paths. It is most applicable when an agent needs to produce reusable configuration and workflow guidance before downstream avatar generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow enables voice and likeness cloning, which can be misused if the person has not consented. <br>
Mitigation: Use only authorized reference audio, photos, and personas, and keep consent records for any cloned voice or likeness. <br>
Risk: Some persona and style presets can produce official-looking or misleading digital humans. <br>
Mitigation: Avoid government or official-looking outputs unless they are clearly fictional, authorized, or labeled as synthetic. <br>
Risk: Cloud platform paths may require API keys and may upload reference media or generated assets to third-party services. <br>
Mitigation: Keep API keys out of configuration files and logs, and review each platform's storage, retention, and data-handling behavior before uploading media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golngod/hutian-opc-digital-avatar) <br>
- [Digital human workflow](references/digital-human-workflow.md) <br>
- [Avatar style presets](references/avatar-style-presets.md) <br>
- [Voice and language guide](references/voice-language-guide.md) <br>
- [Background scenarios](references/background-scenarios.md) <br>
- [OPC persona templates](references/opc-persona-templates.md) <br>
- [Coze platform](https://coze.cn) <br>
- [OPC platform](https://opc.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, inline shell commands, JSON-style configuration, and generated configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide local Python execution or API-key based cloud avatar workflows; final media generation is performed by downstream tools and should be reviewed before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
