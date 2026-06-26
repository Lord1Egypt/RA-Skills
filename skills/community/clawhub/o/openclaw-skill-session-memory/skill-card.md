## Description: <br>
Automatically saves OpenClaw conversations as daily Markdown files with sensitive data redacted and supports keyword search across recent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QiaoTuCodes](https://clawhub.ai/user/QiaoTuCodes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to keep searchable local memory of agent conversations, organized by date, while applying pattern-based redaction to common personal data and secret formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation memory files may retain private, regulated, or business-sensitive session content even after automatic redaction. <br>
Mitigation: Install only when searchable local memory is desired, and periodically review or delete the generated memory files. <br>
Risk: Pattern-based redaction reduces common secrets and personal data but does not guarantee that every sensitive value is removed. <br>
Mitigation: Avoid recording sensitive sessions when possible and manually inspect stored logs before sharing or retaining them long term. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/QiaoTuCodes/openclaw-skill-session-memory) <br>
- [Publisher Profile](https://clawhub.ai/user/QiaoTuCodes) <br>
- [README.md](artifact/README.md) <br>
- [README-CN.md](artifact/README-CN.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown files and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores redacted conversation logs by date and returns keyword search matches with nearby context.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
