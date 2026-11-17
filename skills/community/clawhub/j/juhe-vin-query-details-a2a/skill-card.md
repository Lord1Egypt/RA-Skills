## Description:

Queries Juhe Data's precise VIN vehicle-information API to return make, model, configuration, powertrain, dimensions, and related vehicle profile details through a paid Alipay A2M flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up vehicle profile and configuration details for a specific valid VIN, including checks for used-car, finance, and insurance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install and enable Alipay payment capabilities through an unpinned @latest npx package.

Mitigation: Before installation, confirm the Alipay payment package source is trusted and prefer a pinned, reviewed package version.

Risk: The skill handles VIN values and paid payment handoff data.

Mitigation: Collect only a valid VIN after user consent, send it only to the documented Juhe endpoint, and avoid logging full VINs or complete payment response payloads.

Risk: Vehicle profile data from the third-party service may be incomplete, delayed, or unsuitable as the sole basis for decisions.

Mitigation: Present results as reference information and direct users to verify against official vehicle registration or manufacturer records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-vin-query-details-a2a)
- [Juhe VIN query API endpoint](https://apis.juhe.cn/a2a/query)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown tables populated from Juhe VIN query result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid 17-character VIN and a paid Alipay A2M flow; no-record responses use a separate Markdown template.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
