## Description:

Fetch Oura Ring readiness/sleep + 7-day readiness trends via Oura Cloud API V2, and generate a Morning Readiness Brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sameerbajaj](https://clawhub.ai/user/sameerbajaj)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to retrieve Oura Ring readiness, sleep, resilience, stress, and short-term trend data from the Oura Cloud API, then produce raw JSON/text outputs or a concise morning readiness brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Base URL overrides can direct authenticated Oura API requests away from the official HTTPS Oura host.

Mitigation: Restrict live API calls to the official Oura host unless a reviewed deployment explicitly permits an alternate endpoint.

Risk: Embedding API JSON into generated Python source can mishandle untrusted data and may run unwanted code.

Mitigation: Pass API responses as data through files, stdin, or structured arguments instead of interpolating JSON into executable source.

Risk: Probe scripts include hard-coded local paths for loading credentials.

Mitigation: Remove the probe scripts from release artifacts or rewrite them to use documented environment configuration only.

Risk: Oura bearer tokens can expose sensitive health data if stored or handled loosely.

Mitigation: Use a safer secret mechanism or strict local file permissions, and avoid committing token-bearing environment files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sameerbajaj/skills/oura-ring-skill)
- [Oura API base endpoint](https://api.ouraring.com/v2/usercollection)
- [Oura OAuth applications](https://cloud.ouraring.com/oauth/applications)
- [Oura OAuth token endpoint](https://api.ouraring.com/oauth/token)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [JSON or text from the CLI, and Markdown-like text from the morning brief wrapper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Oura API bearer token for live API calls; mock mode is available for local verification without a token.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
