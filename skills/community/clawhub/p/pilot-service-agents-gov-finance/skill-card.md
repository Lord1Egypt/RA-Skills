## Description:

Government economic and financial records covering SEC EDGAR, BLS time series, HTS/USITC tariffs, and US Department of Education data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and analysts use this skill to discover and query Pilot Protocol service agents for public government finance datasets, including SEC company facts and submissions, BLS time series, HTS tariff data, and Department of Education records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and filters are sent over the Pilot Protocol network to reachable service agents.

Mitigation: Install only when the publisher and Pilot Protocol service agents are trusted, and avoid sending sensitive inputs.

Risk: Agent contracts and catalog entries can change over time.

Mitigation: Run a fresh list-agents query and read each target agent's /help contract before requesting data.

Risk: Natural-language summaries may be generated prose rather than primary-source output.

Mitigation: Use /data instead of /summary when primary-source or structured records are required.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-gov-finance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to use pilotctl commands and read JSON inbox responses from reachable Pilot Protocol service agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
