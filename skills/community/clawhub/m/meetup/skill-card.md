## Description: <br>
Find nearby OpenClaw meetups and related AI/agent community events, summarize the best matches, and help with reminder or share-ready text for local event discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClawNewsde](https://clawhub.ai/user/ClawNewsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find upcoming OpenClaw or AI/agent community events near a specified location, rank a short list, and draft share or reminder text. It is intended for event discovery and planning, with explicit approval required before any persistent, scheduled, or outbound action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location and preference data could be stored more precisely or for longer than needed when ongoing tracking is enabled. <br>
Mitigation: Store only the minimum useful preferences, prefer city-level location, and confirm the city, radius, scope, and reminder behavior before enabling persistence. <br>
Risk: Users could misunderstand a reminder or background check as active before it has actually been created. <br>
Mitigation: Confirm the event and reminder timing, create reminders only when the runtime supports scheduling and the user approves, and state clearly when only manual reminder text was produced. <br>
Risk: Event search may surface stale, duplicate, or thin listings. <br>
Mitigation: Keep only future events with concrete date, location, and event-page evidence, rank by relevance and evidence quality, and state uncertainty instead of inventing missing details. <br>


## Reference(s): <br>
- [Ranking and Selection](references/ranking.md) <br>
- [Source Strategy](references/sources.md) <br>
- [State and Reminders](references/state-and-reminders.md) <br>
- [Meetup Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with event summaries, ranked shortlists, share-ready drafts, reminder prompts, and status or help responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a location and event scope for discovery; reminders, scheduling, saved preferences, and outbound sharing require explicit user approval and runtime support.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
