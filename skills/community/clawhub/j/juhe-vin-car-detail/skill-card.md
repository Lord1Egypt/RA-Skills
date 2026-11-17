## Description:

Looks up detailed vehicle factory information from a 17-character VIN using the Juhe VIN vehicle information API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to validate a VIN and retrieve vehicle make, series, model year, configuration, powertrain, emissions, dimensions, tire, gearbox, announcement number, and wheelbase data for vehicle identification or used-car configuration checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: VINs and the Juhe API key are sent to Juhe for lookup.

Mitigation: Use the skill only when sending VIN lookup data to Juhe is acceptable for the user and use case.

Risk: Passing the Juhe key with --key or in GET URLs can expose it in command history, process listings, or logs.

Mitigation: Prefer JUHE_VIN_CAR_DETAIL_KEY as an environment variable or a protected local secret file, and rotate the key if exposure is suspected.

Risk: Queries may consume Juhe billing quota or paid calls.

Mitigation: Confirm account quota, billing expectations, and application approval before repeated or automated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-vin-car-detail)
- [Juhe VIN vehicle information API documentation](https://www.juhe.cn/docs/api/id/862)
- [Juhe API provider homepage](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text vehicle summary followed by JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_VIN_CAR_DETAIL_KEY credential; sends the VIN and API key to Juhe for lookup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
