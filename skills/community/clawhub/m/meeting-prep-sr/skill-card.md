## Description: <br>
Pull upcoming calendar events, generate agendas, prepare briefing docs, surface relevant context. Never walk into a meeting unprepared. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and external users ask their agent to prepare concise meeting briefs from accessible calendar events and related workspace context. The skill helps generate agendas, surface relevant notes, list preparation items, and track follow-ups before meetings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting briefs may include sensitive calendar, attendee, email, note, or document context available to the agent. <br>
Mitigation: Specify the exact event and allowed sources, exclude email or documents when unnecessary, and review the generated brief before sharing it. <br>
Risk: Locally stored meeting briefs may retain sensitive information after preparation. <br>
Mitigation: Delete or secure locally stored outputs that should not be retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/meeting-prep-sr) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown meeting brief with agenda, context notes, and prep checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses calendar events and optional local workspace context already available to the agent platform; no separate OAuth setup or credentials are required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
