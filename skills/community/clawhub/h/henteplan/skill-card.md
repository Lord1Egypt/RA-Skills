## Description:

Look up Norwegian waste collection schedules — find your provider, search your address, and get upcoming pickup dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henrikkvamme](https://clawhub.ai/user/henrikkvamme)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find the Norwegian waste provider for a postal code or city, search a household address, and retrieve upcoming pickup dates or an iCal subscription URL.

### Deployment Geography for Use:

Norway

## Known Risks and Mitigations:

Risk: Address searches and schedule lookups may send location-related queries to henteplan.no and may save a provider or locationId for future use.

Mitigation: Share only the address information needed for the lookup, and avoid saving or reusing provider/locationId values unless the user wants faster future lookups.

Risk: Optional daily reminders can create recurring automation that continues after the immediate lookup task is complete.

Mitigation: Create cron or HEARTBEAT reminders only after user confirmation, and review or remove them when reminders are no longer needed.

## Reference(s):

- [Henteplan API](https://henteplan.no)
- [Henteplan Skill on ClawHub](https://clawhub.ai/henrikkvamme/skills/henteplan)
- [Publisher Profile](https://clawhub.ai/user/henrikkvamme)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include grouped pickup dates, address disambiguation options, iCal subscription URLs, and optional reminder setup instructions.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
