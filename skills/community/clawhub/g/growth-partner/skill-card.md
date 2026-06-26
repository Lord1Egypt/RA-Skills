## Description: <br>
Growth Partner monitors authorized Feishu messages, group mentions, selected work groups, documents, and calendar events to assemble timelines, insights, and action recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cscguochang](https://clawhub.ai/user/cscguochang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual Feishu workspace users use this skill to track work communications, connect messages with documents and calendar events, and receive concise summaries, risk alerts, drafts, and next-action suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring monitoring can expose private Feishu chats, group messages, documents, calendars, and local logs beyond the intended scope. <br>
Mitigation: Install only for authorized workspace data, verify user and chat IDs, narrow monitored sources and lookback windows, and define log review and deletion practices before enabling scheduled runs. <br>
Risk: Insights or recommendations may misattribute speakers, locations, timing, or whether a discussion is final. <br>
Mitigation: Require summaries and action recommendations to cite key sources and distinguish speaker, channel, time, and discussion status before delivery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cscguochang/growth-partner) <br>
- [Publisher Profile](https://clawhub.ai/user/cscguochang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown summaries, action recommendations, risk alerts, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local memory logs for insights and delivery history when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
