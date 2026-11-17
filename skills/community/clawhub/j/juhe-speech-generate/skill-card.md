## Description:

AI语音合成TTS - 聚合数据 generates speech audio and downloadable audio links from text through Juhe's text-to-speech API, with selectable voices and languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert short text into synthesized speech, choose a supported voice or language, and return either a temporary audio URL or a downloaded audio file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed if passed on the command line or stored in scripts/.env.

Mitigation: Set JUHE_SPEECH_KEY through environment or platform secrets and avoid logging command arguments that contain keys.

Risk: Text submitted for synthesis is sent to Juhe's service and may include sensitive content.

Mitigation: Do not synthesize confidential text unless the user has approved sending it to Juhe.

Risk: Downloaded audio can create or replace files at user-selected paths.

Mitigation: Use --download or --output only for paths the user intends to create or replace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-speech-generate)
- [Juhe AI Speech Synthesis TTS API documentation](https://www.juhe.cn/docs/api/id/830)
- [Juhe Data](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands, generated audio URLs, and optional local audio file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUHE_SPEECH_KEY; input text is limited to 500 characters and generated audio links are temporary.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
