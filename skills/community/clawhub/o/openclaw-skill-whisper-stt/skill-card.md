## Description:

Converts audio files to text with OpenAI Whisper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaotucodes](https://clawhub.ai/user/qiaotucodes)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to transcribe audio or voice files, including Chinese-language audio, into text through a local Whisper-based workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio may contain private, business, medical, legal, or regulated information.

Mitigation: Review inputs before use and install or run the skill only in environments approved for that data.

Risk: The skill instructions describe forwarding transcripts to Feishu without clear destination, consent, or implementation details.

Mitigation: Confirm the forwarding destination and consent model before deployment, or remove or disable transcript forwarding.

Risk: Whisper model and dependency installation can download large artifacts and execute local transcription code.

Mitigation: Use a pinned virtual environment and choose the smallest model that satisfies accuracy requirements.

## Reference(s):

- [OpenAI Whisper](https://github.com/openai/whisper)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub skill page](https://clawhub.ai/qiaotucodes/skills/openclaw-skill-whisper-stt)
- [ClawHub publisher profile](https://clawhub.ai/user/qiaotucodes)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text transcripts, Markdown guidance, Python code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write a transcript to an output file when invoked with the CLI output option.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
