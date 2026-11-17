## Description:

MOSS TTSD 多人对话合成 generates a single continuous WAV dialogue from 1-5 speaker-tagged text turns using MOSI Studio voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkkb473](https://clawhub.ai/user/mkkb473)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate multi-speaker dialogue audio from role-tagged scripts for conversational content, testing, and voice workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dialogue text is sent to MOSI Studio for audio generation.

Mitigation: Use the skill only for text that may be shared with MOSI Studio and avoid submitting confidential or regulated content unless that use is approved.

Risk: Passing the API key with --api-key can expose the secret through shell history or process inspection.

Mitigation: Set MOSI_TTS_API_KEY through a protected environment or secret manager.

Risk: The helper script writes the generated WAV file to the selected output path.

Mitigation: Choose an output path intentionally and verify it does not overwrite or expose sensitive local files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkkb473/skills/moss-ttsd)
- [MOSI Studio homepage](https://studio.mosi.cn)
- [MOSI speech API endpoint](https://studio.mosi.cn/api/v1/audio/speech)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; the helper script writes a WAV audio file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOSI_TTS_API_KEY, curl, jq, and base64; supports 1-5 speakers and writes WAV output to the configured path.]

## Skill Version(s):

2.0.0 (source: server release metadata, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
