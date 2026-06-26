## Description: <br>
Fetches and presents monday.com Notetaker meeting notes or prepares the user for their next meeting using calendar context and related past meeting history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees use this skill to retrieve, summarize, and review their own monday.com Notetaker meetings by person, topic, date, or recency. It can also prepare the user for the next meeting by combining Google Calendar event context with related past meeting notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access local Google Calendar credentials, calendar events, attendees, and monday.com Notetaker data. <br>
Mitigation: Install only when this data access is expected, review the local .context file before use, and keep access scoped to OWN unless broader access is explicitly needed. <br>
Risk: The skill can optionally create monday.com board items from meeting action items. <br>
Mitigation: Approve item creation only after confirming the target board, item names, owners, and due dates. <br>
Risk: Meeting notes may contain sensitive personal or business information. <br>
Mitigation: Use the skill only in contexts where the requester is authorized to view the relevant meeting data, and avoid fetching full transcripts unless explicitly requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/meeting-notetaker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with meeting summaries, prep notes, action-item prompts, and occasional shell or API command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in the user's language, omits empty sections, prefers recent matching meetings, and avoids fetching full transcripts unless explicitly asked.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
