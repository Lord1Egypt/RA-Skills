## Description:

Converts user-provided text into AI speech, voiceover, or text-to-audio output through the Giggle.pro TTS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate spoken audio or voiceover from text after selecting a voice, emotion, and speaking rate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is sent to giggle.pro and full prompts may be stored locally in task log files.

Mitigation: Avoid secrets or sensitive text, and review or remove local prompt logs according to the deployment's retention requirements.

Risk: The skill forwards service output, including audio links and status text, directly to the user.

Mitigation: Review generated links and returned messages before relying on them in sensitive workflows.

Risk: Security evidence marks the release suspicious because task-id validation, URL validation, and cleanup behavior need tightening.

Mitigation: Install only after accepting these risks or after adding validation and cleanup controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/patches429/skills/giggle-generation-speech)
- [Giggle.pro Service](https://giggle.pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status messages with audio links and JSON task status during polling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, and GIGGLE_API_KEY; writes task state logs under ~/.openclaw/skills/giggle-generation-speech/logs/ and may register a 30 second polling job.]

## Skill Version(s):

0.0.10 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
