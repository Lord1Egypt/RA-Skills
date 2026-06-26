## Description: <br>
Yunshi is a bilingual Chinese astrology and fortune-telling skill for BaZi, ZiWei DouShu, QiMen DunJia, I Ching divination, marriage compatibility, feng shui, and daily fortune readings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Yunshi to generate personal Chinese astrology readings, chart calculations, divination guidance, compatibility reports, feng shui suggestions, and scheduled daily fortune messages. The skill can store birth and family profile data for personalized readings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive birth details, names, and family relationship data in local profile files. <br>
Mitigation: Use the skill only in a private or isolated workspace, restrict access to profile files, and avoid storing real personal data unless users understand retention and deletion limits. <br>
Risk: Scheduled fortune pushes can run unattended and may expose sensitive readings or profile-derived details in runtime output or logs. <br>
Mitigation: Review cron settings before enabling pushes, disable unattended pushes when not needed, and limit logging for profile-linked readings. <br>
Risk: Agent prompts associated with scheduled pushes may use web search, local command execution, and preference tracking. <br>
Mitigation: Disable web-enabled or command-running push flows in environments where unattended actions are not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiajiaoy/mingshi) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Registration Flow](docs/注册流程.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with optional shell commands and JSON profile data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese and English responses; may read and write local profile, preference, and push-log files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
