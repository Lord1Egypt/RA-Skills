## Description:

Query package/express tracking worldwide via unified API. Integrates with Kdniao and is extensible to other providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to track parcels, query logistics information, or integrate courier tracking through a Python package and CLI backed by Kdniao.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live tracking can involve real shipment numbers, phone suffixes, and production Kdniao credentials.

Mitigation: Review the skill and configuration before installation, and use only the minimum shipment and customer data required for a query.

Risk: Sandbox mode uses a plaintext HTTP endpoint that can expose shipment details or credential-derived request data in transit.

Mitigation: Avoid sandbox mode for sensitive data and restrict configuration to trusted HTTPS Kdniao endpoints for production use.

## Reference(s):

- [Package Tracker project homepage](https://github.com/openlang-cn/package-tracker.git)
- [Kdniao tracking API documentation](https://www.kdniao.com/api-track)
- [ClawHub skill page](https://clawhub.ai/openlang-cn/skills/package-track)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; the CLI can emit human-readable text or JSON tracking results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and Kdniao credentials for live tracking; configuration is stored in package_tracker.json.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
