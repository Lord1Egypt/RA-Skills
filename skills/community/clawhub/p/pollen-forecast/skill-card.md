## Description: <br>
Daily pollen forecast and allergy alerts for Chinese cities. Use when user asks about pollen levels, allergy season, hay fever, flower pollen, 花粉, 过敏, or wants to set up daily pollen alerts. Supports Beijing, Shanghai, Guangzhou, and other major Chinese cities. Can create automated daily cron reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yuchen-Lju](https://clawhub.ai/user/Yuchen-Lju) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search for current pollen levels in major Chinese cities, format concise daily allergy reports, and optionally prepare a scheduled daily alert. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled alerts can create recurring notifications to an unintended channel or recipient if enabled casually. <br>
Mitigation: Confirm the city, timezone, schedule, destination channel, and recipient before creating the cron job, and keep instructions available to list or delete the job later. <br>
Risk: Pollen forecasts may be stale or incomplete when sourced through search. <br>
Mitigation: Search for current city-specific data at report time and make the report date and forecast window explicit. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional shell command block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are city- and date-specific pollen summaries with optional OpenClaw cron configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
