## Description:

OpenClaw Feishu Optimizer helps OpenClaw agents handle Feishu voice and text messages by transcribing audio, formatting message text, and preparing optimized replies.

This skill is for research and development only.

## Publisher:

[huangshaoshuai123](https://clawhub.ai/user/huangshaoshuai123)

### License/Terms of Use:


## Use Case:

OpenClaw users and Feishu bot maintainers use this skill to convert Feishu voice-message audio into text, normalize message formatting, and save or print processing results for agent replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio may be sent to Google Speech Recognition, which can expose private Feishu conversations or regulated audio to external processing.

Mitigation: Use only with explicit user or administrator consent, avoid sensitive audio unless Google processing is acceptable, and review cloud transcription requirements before deployment.

Risk: Automatic message handling can process Feishu content without clearly defined consent or privacy boundaries.

Mitigation: Limit use to approved conversations, document the bot behavior for users, and store generated outputs only in protected locations.

Risk: Dependencies are listed without pinned versions.

Mitigation: Install in an isolated Python environment and pin reviewed versions of SpeechRecognition and pydub before operational use.

## Reference(s):

- [Artifact README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/huangshaoshuai123/skills/openclaw-feishu-optimizer)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text status messages and transcription results, optional JSON result files, and Markdown documentation with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Speech recognition output depends on local audio conversion and Google Speech Recognition availability.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
