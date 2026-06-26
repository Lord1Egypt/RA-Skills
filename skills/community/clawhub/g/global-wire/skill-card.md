## Description: <br>
GlobalWire turns answers about major world events into wire-style briefings, rolling event timelines, verification notes, and alert bullets with stable formatting, source priority, and confidence labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yly46967-source](https://clawhub.ai/user/yly46967-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use GlobalWire to turn major world-news questions or rough answers into concise wire-style briefings, rolling timelines, alerts, and claim-reliability checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad news questions and apply its own source-priority hierarchy, which may not match a user's intended scope or preferred sources. <br>
Mitigation: Specify the topic, region, time window, and required sources when precision matters, and review the source list before relying on the briefing. <br>
Risk: The skill may create local Markdown archives for repeatable or archival workflows. <br>
Mitigation: Request chat-only output or confirm the destination path before asking the agent to save briefs, alerts, timelines, or snapshots. <br>
Risk: Credibility labels grade answer reliability and do not replace full fact-checking for high-stakes or fast-moving claims. <br>
Mitigation: Cross-check important claims against primary materials or reputable reporting, especially when the output marks items as developing, weak, or needing cross-verification. <br>


## Reference(s): <br>
- [GlobalWire release page](https://clawhub.ai/yly46967-source/global-wire) <br>
- [Output Modes](references/output-modes.md) <br>
- [Timeline Rules](references/timeline-rules.md) <br>
- [Credibility Rules](references/credibility-rules.md) <br>
- [Source Priority](references/source-priority.md) <br>
- [Formatting Rules](references/formatting-rules.md) <br>
- [File Layout](references/file-layout.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown briefings, timelines, verification notes, and alerts; optional saved Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates facts from analysis, applies confidence labels, uses source-priority guidance, and localizes visible labels for Chinese requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
