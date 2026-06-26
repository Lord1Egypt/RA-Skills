## Description: <br>
Oasis Audio Pro generates personalized AI audio narration with background music from a user's request and optional local OpenClaw/QClaw context, sending only a composed prompt to xplai.ai for generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[littlelightsai](https://clawhub.ai/user/littlelightsai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn requests, notes, long content, or recent life events into personalized narrated audio with background music. It can personalize output with recent local OpenClaw/QClaw context when the user accepts that boundary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read recent OpenClaw/QClaw sessions, memory files, and USER.md for personalization. <br>
Mitigation: Install and run it only when that local read access is acceptable; use dry-run previews before sending generated prompts. <br>
Risk: The composed prompt sent to xplai.ai may contain inferred personal details derived from local context. <br>
Mitigation: Review sanitized previews, require explicit confirmation before sensitive sends, and redact hard secrets before transmission or audit logging. <br>
Risk: Debug or audit modes can expose prompt or request details locally. <br>
Mitigation: Avoid --audit and --debug for sensitive content unless local traceability is explicitly needed and the resulting files are protected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/littlelightsai/oasis-audio-pro) <br>
- [xplai.ai](https://www.xplai.ai/) <br>
- [Audio modes reference](audio_modes.md) <br>
- [Text architecture reference](text_architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON previews, audio IDs, status text, and generated audio URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a single-narrator MP3 with background music through xplai.ai; dry-run mode previews the sanitized outbound prompt without sending it.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
