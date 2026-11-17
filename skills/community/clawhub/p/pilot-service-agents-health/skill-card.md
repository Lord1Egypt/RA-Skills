## Description:

Helps agents query public-health and biomedical service agents for ClinicalTrials.gov, openFDA, CDC, WHO, ClinVar, DailyMed, and disease.sh data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and data-focused agents use this skill to discover and query public health and biomedical service agents for clinical trials, drug labels, adverse events, surveillance indicators, disease statistics, and related public records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake public biomedical records or generated summaries for medical advice.

Mitigation: Use the skill for public data retrieval only, avoid diagnostic advice, and require qualified review before applying outputs to health decisions.

Risk: Pilot Protocol service-agent availability, catalog contents, and upstream public data sources can change.

Mitigation: Run fresh list-agents discovery and request /help from the selected agent before sending data queries.

Risk: The catalog snapshot includes some agents outside the core health scope, such as food recall, exercise, or tides data.

Mitigation: Select hosts intentionally and avoid unrelated listed agents unless that data source is explicitly needed.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-health)
- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on public data queries through Pilot Protocol service agents; service-agent responses may include JSON envelopes, plain-text help, or generated summaries.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
