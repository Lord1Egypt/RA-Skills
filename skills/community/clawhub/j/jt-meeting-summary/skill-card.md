## Description: <br>
Pure prompt guidance for generating faithful meeting and call summaries, including meeting minutes, concise summaries, ten-minute summaries, speaker summaries, action items, titles, tags, and visual-summary prompts without calling external APIs or tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quent1nq](https://clawhub.ai/user/quent1nq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn meeting or call transcripts into faithful structured summaries, minutes, action items, speaker views, titles and tags, or visual-summary prompts. It is especially suited to Chinese meeting-summary workflows that require explicit handling of missing facts, speaker attribution, decisions, deadlines, and unresolved questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting and call transcripts can contain sensitive personal or business information, including phone numbers. <br>
Mitigation: Use the skill only with transcripts suitable for model processing, and request phone-number masking or other redaction when identifiers are not required. <br>
Risk: The skill defaults to Chinese-oriented summary structures and may not preserve a different output language unless requested. <br>
Mitigation: Ask explicitly for the desired output language when the transcript or downstream workflow should remain non-Chinese. <br>
Risk: Summaries can mislead if speaker attribution, deadlines, or decisions are inferred beyond the transcript. <br>
Mitigation: Follow the skill rules to preserve speaker names, mark missing owners or times as unclear, and self-check every speaker, task owner, deadline, and conclusion against the transcript. <br>


## Reference(s): <br>
- [Phone-call summary](references/call-summary.md) <br>
- [Concise minutes Markdown](references/concise-minutes.md) <br>
- [Full meeting minutes JSON](references/full-minutes-json.md) <br>
- [Summary components](references/summary-components.md) <br>
- [Ten-minute / long-meeting summary](references/ten-minute-summary.md) <br>
- [Visual / comic summary prompt](references/visual-summary-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown, strict JSON for formal minutes, or text-to-image prompt text depending on the selected mode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only output; no external API, database, workflow service, retrieval tool, or image-generation call is performed unless the user separately asks for it.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
