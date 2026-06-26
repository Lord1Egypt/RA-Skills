## Description: <br>
朱批录 helps civil-service exam candidates record daily practice, classify wrong-answer screenshots, track weak modules, generate short study summaries, export Excel wrong-question books, and optionally sync selected records to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KaguraNanaga](https://clawhub.ai/user/KaguraNanaga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and study agents use this skill to turn chat messages and exam screenshots into structured civil-service exam practice records, review reminders, concise feedback, and exportable study materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Study screenshots, notes, performance records, and inferred mood may be stored locally, sent to a configured multimodal model, included in exports, or uploaded to Feishu when sync is enabled. <br>
Mitigation: Use a dedicated workspace or channel, avoid unrelated or sensitive images, keep Feishu sync disabled unless needed, and prefer exports without embedded screenshots for sensitive material. <br>
Risk: The release makes local-only privacy claims, but optional model recognition, Excel export with images, and Feishu sync can move data outside local storage. <br>
Mitigation: Review the configured model provider, Feishu credentials, export options, and destination documents before processing personal study materials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KaguraNanaga/kaogong-study-tracker) <br>
- [Tone guide](references/tone_guide.md) <br>
- [Reply templates](references/reply_templates.md) <br>
- [Workspace example](assets/workspace-example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Short chat replies, JSON records, Excel exports, Markdown-style guidance, JavaScript/Python command outputs, and Feishu document updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are intended to stay concise; exports may include embedded screenshots when enabled.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
