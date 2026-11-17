## Description:

Put a real alarm on your person's phone, and on their friends', family's or community's phones, through LFG Alarm's MCP server (https://mcp.lfg.gm). Set, share and change alarms that ring together. Use it when someone asks to be woken, reminded loudly, or rung for a moment: a time, an event from a Luma or Partiful link, an account posting on X, a stream going live, a token hitting a price, or a webhook being called; or when they want a group, a partner or a family rung together at the same moment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lfg](https://clawhub.ai/user/lfg)

### License/Terms of Use:

MIT-0

## Use Case:

External users connect an AI agent to LFG Alarm to create, share, and manage phone alarms for times, events, online activity, price changes, or webhook calls. The skill also helps users coordinate alarms with friends, family, or communities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared alarms can expose the alarm to more people than intended.

Mitigation: Default to private visibility, confirm intended recipients and reach, and review the names before adding people.

Risk: A webhook alarm link can be used by anyone who obtains the private link to trigger the alarm.

Mitigation: Keep webhook links private and share them only with trusted systems.

Risk: Connecting the service authorizes management of alarms and related social features, and recurring alarms may continue after they are no longer needed.

Mitigation: Review the requested action and alarm settings, and disable or delete recurring alarms when they are no longer needed.

## Reference(s):

- [LFG Alarm agent setup](https://lfg.gm/agents)
- [LFG Alarm AI agent guide](https://lfg.gm/wiki/ai-agents)
- [LFG Alarm on ClawHub](https://clawhub.ai/lfg/skills/lfg-alarm)

## Skill Output:

**Output Type(s):** [API Calls, Configuration, Guidance]

**Output Format:** [Alarm creation and management actions with text guidance and share links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions are performed through the connected LFG Alarm service; generated alarms may include a share link and related share materials.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
