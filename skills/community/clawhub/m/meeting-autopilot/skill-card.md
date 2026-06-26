## Description: <br>
Turn meeting transcripts into operational outputs - action items, decisions, follow-up email drafts, and ticket drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and operators use this skill to process meeting transcripts into decisions, action items, open questions, follow-up email drafts, and ticket drafts. It is intended for transcript-driven meeting follow-up, not audio transcription or automatic email/ticket submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts and extracted meeting details may be sent to the configured Anthropic or OpenAI endpoint. <br>
Mitigation: Use the skill only for meetings that your organization permits sending to external AI services. <br>
Risk: Extracted meeting history is saved locally by default. <br>
Mitigation: Use --no-history for sensitive meetings or delete ~/.meeting-autopilot/history/ after processing. <br>
Risk: Generated email and ticket drafts may omit context or require judgment before sharing. <br>
Mitigation: Review generated drafts before sending emails or creating tickets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tkuehnl/meeting-autopilot) <br>
- [README](README.md) <br>
- [Security model](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with structured sections, tables, follow-up email drafts, and ticket drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally save Markdown reports and extracted meeting history as local files.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
