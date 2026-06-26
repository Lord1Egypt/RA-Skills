## Description: <br>
This skill helps an agent use the ofw-mcp MCP server for OurFamilyWizard co-parenting messages, calendar events, shared expenses, and journal entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to OurFamilyWizard data, check messages and calendar items, manage expenses, and draft or send OFW records with explicit review for sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration handles sensitive OurFamilyWizard credentials and co-parenting records with read/write access. <br>
Mitigation: Install only in trusted environments, store credentials carefully, and review messages or records before any write action. <br>
Risk: Reading notifications or unread messages may update OFW state, including last-seen or read status. <br>
Mitigation: Avoid silent background reads and warn the user before calls that can change message or notification state. <br>
Risk: Synced OFW data may remain in a local cache. <br>
Mitigation: Use explicit OFW requests, limit access to trusted machines, and remove cached data when it is no longer needed. <br>


## Reference(s): <br>
- [ofw-mcp npm package](https://www.npmjs.com/package/ofw-mcp) <br>
- [ofw-mcp project link declared in artifact](https://github.com/chrischall/ofw-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MCP tool calls that read or write OurFamilyWizard records.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
