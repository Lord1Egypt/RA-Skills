## Description: <br>
Manages accountability items on a configured Monday.com board for item creation, status checks, work sessions, and owner-assigned accountability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novalystrix](https://clawhub.ai/user/novalystrix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure an agent to create, review, update, and work through accountability items on a Monday.com board, including cron-triggered work sessions and daily summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run recurring autonomous work sessions that change Monday.com data, contact people, and delegate tasks. <br>
Mitigation: Install only when scheduled autonomous accountability work is intended, and require human approval before outreach, configuration changes, Done status transitions, or spawning sub-agents. <br>
Risk: A broadly scoped Monday.com token could expose or modify more board data than intended. <br>
Mitigation: Use a least-privileged Monday.com token restricted to the intended board and required operations. <br>
Risk: Sensitive information placed in accountability item details could be read by the agent or passed into delegated work. <br>
Mitigation: Avoid storing secrets or unnecessary sensitive information in Monday.com item details, updates, and sub-agent task context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/novalystrix/monday-accountability) <br>
- [Monday.com API v2 endpoint](https://api.monday.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with GraphQL and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Monday.com API token, board ID, and column IDs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
