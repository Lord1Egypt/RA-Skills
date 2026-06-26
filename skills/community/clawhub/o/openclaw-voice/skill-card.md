## Description: <br>
OpenClaw Voice manages CLI-based voice conversations, transcripts, searchable history, ElevenLabs voice profiles, backups, and generated interchange Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frank-bot07](https://clawhub.ai/user/frank-bot07) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to record and organize voice conversation context, manage transcript history, configure voice profiles, and publish local Markdown context for other agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcripts, summaries, voice profile descriptions, backups, and interchange Markdown are persistent local records that may contain sensitive information. <br>
Mitigation: Avoid storing secrets or private data in those records, and review generated files before sharing or using them as agent context. <br>
Risk: Generated interchange Markdown may be consumed by other agents as context. <br>
Mitigation: Review generated interchange files before relying on them in downstream agent workflows. <br>
Risk: The skill uses a local SQLite database and npm dependencies. <br>
Mitigation: Install only in environments where local persistence and dependency installation are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frank-bot07/openclaw-voice) <br>
- [README.md](artifact/README.md) <br>
- [VOICE_CALLING_SPEC.md](artifact/VOICE_CALLING_SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [CLI text, Markdown interchange files, SQLite records, JSON profile settings, and backup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists transcripts, summaries, voice profile descriptions, backups, and generated interchange Markdown as local records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
