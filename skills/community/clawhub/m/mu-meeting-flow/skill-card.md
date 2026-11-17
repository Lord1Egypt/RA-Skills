## Description:

A meeting workflow skill that helps an agent schedule meetings, prepare agendas and materials, guide facilitation, extract minutes and TODOs from notes or transcripts, and manage follow-up through configurable workplace-tool adapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT

## Use Case:

Employees, external collaborators, and agent operators use this skill to turn meeting requests into an end-to-end workflow covering scheduling, room booking, preparation, live facilitation, minutes, TODO tracking, and follow-up. It is intended for meeting workflows rather than general task management outside a meeting context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may act across connected calendars, rooms, documents, transcripts, TODO stores, and notification systems.

Mitigation: Use least-privilege adapter accounts and require preview and confirmation before calendar, room, document, transcript, TODO, or notification actions are sent or saved.

Risk: Adapter configuration can expose credentials or API tokens if real secrets are stored directly in config/adapters.json.

Mitigation: Use a secret manager or environment references for credentials, and avoid committing real secrets in adapter configuration files.

Risk: Meeting notes, transcripts, and follow-up notifications can contain sensitive workplace information.

Mitigation: Review generated minutes, TODOs, and notification drafts before sharing them, and restrict adapter access to the intended workspace or document scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muippt/skills/mu-meeting-flow)
- [Integration rules](references/integration-rules.md)
- [Meeting methodology](references/methodology.md)
- [TODO pool](references/todo-pool.md)
- [FAQ](references/faq.md)
- [Adapter configuration example](config/adapters.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown and structured text with optional configuration JSON guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include invite details, agendas, facilitation prompts, meeting minutes, TODO lists, notification drafts, and manual fallback instructions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
