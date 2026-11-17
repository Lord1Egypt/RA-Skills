## Description:

朱批录 tracks Chinese civil-service exam study activity by parsing score updates, wrong-question screenshots, check-ins, and review progress, then updating local records and generating concise summaries, exports, and optional Feishu sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagurananaga](https://clawhub.ai/user/kagurananaga)

### License/Terms of Use:

MIT-0

## Use Case:

External users preparing for Chinese civil-service exams use this skill to record daily practice results, classify wrong questions, track weak modules, review pending questions, export study records, and optionally sync selected wrong-question content to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exam screenshots and notes are stored locally and image inputs may be sent to the configured multimodal model provider.

Mitigation: Review the model provider configuration before use, avoid submitting sensitive screenshots, and use the manual text fallback when needed.

Risk: Feishu sync can upload wrong-question data and screenshots outside the local device when the user enables and triggers it.

Mitigation: Enable Feishu sync only with intended app credentials and document permissions; keep the local-only workflow when cloud sync is not acceptable.

Risk: Spreadsheet exports may expose users to untrusted imported content until formula sanitization and temporary-file handling are hardened.

Mitigation: Avoid exporting or opening spreadsheets from untrusted imported content until those export hardening issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kagurananaga/skills/kaogong-study-tracker)
- [OpenClaw](https://openclaw.ai)
- [Reply Templates](references/reply_templates.md)
- [Tone Guide](references/tone_guide.md)
- [Workspace Example](assets/workspace-example.yaml)

## Skill Output:

**Output Type(s):** [text, json, files, configuration, guidance]

**Output Format:** [Conversation replies, local JSON study records, Excel workbook exports, and optional Feishu document updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process user-provided screenshots through the configured multimodal model and may embed screenshots in exports or optional Feishu sync.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
