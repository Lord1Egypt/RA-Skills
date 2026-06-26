## Description: <br>
Orchestration skill that processes raw work-item data from Slack, GitHub, calendar, Notion, Trello, and email, then produces a merged, prioritized action board with owners, due dates, reply drafts, and follow-up questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[honouralexwill](https://clawhub.ai/user/honouralexwill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn caller-supplied Slack, GitHub, calendar, Notion, Trello, and email work data into a consolidated draft action board for prioritization and follow-up planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The action board depends on raw work data supplied by upstream tools, so it may be incomplete when a source is unavailable or omitted. <br>
Mitigation: Review skipped-source notes and verify important items against the original source links before acting. <br>
Risk: Suggested actions and reply drafts can be incorrect or misleading if the supplied source data is stale, partial, or ambiguous. <br>
Mitigation: Treat outputs as drafts, review the original context, and require explicit confirmation before any write-back or message is sent. <br>
Risk: Upstream connectors may introduce separate credential, API, or data-access risks outside this skill's local processing behavior. <br>
Mitigation: Review upstream connectors separately before providing Slack, GitHub, calendar, Notion, Trello, or email data to the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/honouralexwill/inbox-to-action-closer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown action board plus structured JSON action board data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft-only action items grouped by urgency, with source links, owners, due dates, reply drafts, follow-up questions, skipped-source notes, and item counts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
