## Description: <br>
Ken Idea Capture helps an agent silently capture possible user ideas, feature requests, complaints, wishes, and pain points into an inbox for later review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guytogay](https://clawhub.ai/user/guytogay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams use this skill to have an agent notice possible ideas, needs, complaints, and pain points during ordinary conversations, append them to an inbox, and prepare scheduled review summaries for Telegram and Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill silently logs messages that it classifies as ideas, needs, complaints, wishes, or pain points. <br>
Mitigation: Enable it only in conversations where silent capture is expected, confirm the inbox path before use, and keep a clear way to disable capture. <br>
Risk: Captured content may include secrets, personal data, or sensitive business context. <br>
Mitigation: Avoid using the skill in sensitive chats, review captured entries regularly, and provide a deletion path for entries that should not be retained. <br>
Risk: Daily and weekly summaries can forward captured content to Telegram and Feishu. <br>
Mitigation: Confirm the Telegram and Feishu destinations before enabling summaries, and review captured content before forwarding when privacy or confidentiality matters. <br>


## Reference(s): <br>
- [ClawHub Ken Idea Capture Skill Page](https://clawhub.ai/guytogay/ken-idea-capture) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown inbox entries and text review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Silently appends timestamped captures to an inbox path and may send daily or weekly summaries to Telegram and Feishu when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
