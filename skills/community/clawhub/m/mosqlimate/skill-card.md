## Description:

Query Mosqlimate dengue, zika, and chikungunya data, models, and forecasts, and validate or upload predictions with mosqlient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mosqlimate-project](https://clawhub.ai/user/mosqlimate-project)

### License/Terms of Use:

MIT-0

## Use Case:

Public health analysts, epidemiologists, and developers use this skill to retrieve Brazilian arbovirus, climate, mosquito, and vegetation data, search forecasting models, and validate or submit predictions to Mosqlimate.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: An exposed API key could provide access to the user's Mosqlimate account.

Mitigation: Keep MOSQLIMATE_API_KEY in the environment and never print, log, or commit it.

Risk: Forecast data is sent to Mosqlimate when uploaded, including when it is left unpublished; publishing also makes it public.

Mitigation: Validate or dry-run first, review the forecast and visibility, and require explicit confirmation before upload; use --published only when public release is intended.

Risk: A custom API URL could direct credentials or data to an untrusted destination.

Mitigation: Use only a trusted API destination, including when MOSQLIENT_API_URL is overridden.

## Reference(s):

- [Datastore commands](references/datastore.md)
- [Registry commands](references/registry.md)
- [Prediction uploads](references/predictions.md)
- [API endpoints and output schemas](references/api.md)
- [Troubleshooting](references/troubleshooting.md)
- [Mosqlimate API documentation](https://api.mosqlimate.org/docs/)
- [Mosqlimate API OpenAPI document](https://api.mosqlimate.org/api/openapi.json)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Shell commands, Guidance]

**Output Format:** [JSON or CSV data, with Markdown summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Data queries are scoped by disease, dates, and geography; forecast uploads require explicit confirmation and can remain unpublished.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
