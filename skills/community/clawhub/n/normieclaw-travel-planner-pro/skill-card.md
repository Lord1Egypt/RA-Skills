## Description:

Travel Planner Pro helps an agent create day-by-day itineraries, budget estimates, weather-aware packing lists, document checklists, local travel guidance, and shareable trip plans from chat requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to plan trips, compare budgets, prepare packing and document checklists, track local context, and maintain local trip files. It is also intended to support reminder generation and an optional dashboard workflow for visual trip management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional dashboard design can sync sensitive trip, profile, companion, budget, and loyalty data to Supabase despite local-only privacy claims.

Mitigation: Use the chat skill in local mode unless dashboard sync has explicit opt-in, clear transmitted-field disclosure, data minimization, secure access controls, and deletion controls.

Risk: Travel planning can involve sensitive documents, payment references, booking credentials, and personal itinerary details.

Mitigation: Do not provide passport numbers, payment card numbers, booking passwords, or raw document scans; store only limited status fields such as passport expiry or payment last-four references when needed.

Risk: The included reminder and setup scripts are identified by security evidence as needing repair before relying on them.

Mitigation: Review and test scripts in an isolated workspace before execution, and confirm path validation, file permissions, and expected input handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-travel-planner-pro)
- [README](artifact/README.md)
- [Security guidance](artifact/SECURITY.md)
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast)
- [Publisher profile](https://clawhub.ai/user/nollio)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON file schemas, configuration guidance, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local travel profile, trip, budget, packing, share, config, and reminder files.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
