## Description:

Live world-data query engine that queries real-time external APIs for factual ground truth across government data, scholarly literature, weather and hazards, geocoding, finance, macro indicators, court records, nutrition, news events, property records, land due diligence, academic papers, satellite imagery, and product manuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Reach to fetch citation-bearing, current facts from registered external data sources when a task needs a specific measurement, lookup, filing, forecast, alert, paper, or record. It is not intended for open-ended research, person investigations, or synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create third-party API accounts and store issued keys in the active agent profile.

Mitigation: Review account-provisioning settings before installation, restrict account creation to approved sources, and audit stored credentials regularly.

Risk: The skill can start third-party MCP subprocesses and use mutable external runtime dependencies.

Mitigation: Pin MCP package versions, filter subprocess environments, and run the skill in a least-privilege sandbox.

Risk: LinkedIn integration can use an authenticated browser session and includes messaging actions.

Mitigation: Remove or disable LinkedIn messaging actions unless the deployment explicitly requires them and has operator approval.

Risk: Self-update and API-mining behavior can change code or scan recent session history.

Mitigation: Disable self-update and API-mining for routine deployments, or require review before applying updates and before using discovered sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-reach)
- [Source Index](references/sources/index.md)
- [Credential Files](references/credential-files.md)
- [Account Provisioning](references/account_provisioning.md)
- [Usage Tracking](references/usage_tracking.md)
- [Gotchas](references/gotchas.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or JSON responses with citations, status envelopes, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit observation or action journals for query and account-registration activity.]

## Skill Version(s):

1.0.1 (source: ClawHub release); artifact metadata version 3.12.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
