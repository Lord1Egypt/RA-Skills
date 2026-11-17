## Description:

Map service address lookup and distance-query workflow for converting addresses or POIs into coordinates and calculating travel distances with Tencent Location Service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottkiss](https://clawhub.ai/user/scottkiss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external users use this skill to geocode addresses or POIs and estimate travel distance or duration between locations through Tencent Location Service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a third-party binary downloaded from GitHub under their user account.

Mitigation: Install only in an environment where running that binary is acceptable, and independently verify the downloaded CLI before use.

Risk: The workflow can persist a Tencent Location Service API key in a global user config file.

Mitigation: Prefer a restricted or throwaway Tencent key and check or lock down permissions on the global config file.

Risk: Address and location queries may contain sensitive personal location information.

Mitigation: Avoid submitting sensitive personal locations unless the user has accepted that exposure to Tencent Location Service.

## Reference(s):

- [ClawHub Map Address Query Skill Page](https://clawhub.ai/scottkiss/skills/map-address-query-skills)
- [Tencent Location Service Console](https://lbs.qq.com/dev/console/application/mine)
- [qq-map-cli v1.0.2 Linux binary download](https://github.com/scottkiss/qq-map-cli/releases/download/v1.0.2/qq-map-cli-linux-x86_64.zip)
- [qq-map-cli v1.0.2 macOS binary download](https://github.com/scottkiss/qq-map-cli/releases/download/v1.0.2/qq-map-cli-darwin-arm64.zip)
- [qq-map-cli v1.0.2 Windows binary download](https://github.com/scottkiss/qq-map-cli/releases/download/v1.0.2/qq-map-cli-windows-x86_64.zip)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tencent Location Service key; supports human-readable CLI output and raw JSON output for automation.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
