## Description:

Queries KZCloud CXO map locations and returns filtered CXO details by function, grade, position camp, keyword, and distance range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuxiaoxin00](https://clawhub.ai/user/yuxiaoxin00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to authenticate to KZCloud, inspect CXO filter options, resolve a user's location through the Gaode Map LBS dependency, and return nearby CXO records in a fixed table format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The login helper may expose passwords or bearer tokens through command arguments, logs, persistent environment storage, or PowerShell token interpolation.

Mitigation: Review carefully before installing, avoid printing tokens, prompt for passwords securely, avoid persistent token storage unless explicitly accepted, and rotate any exposed token.

Risk: TLS verification is disabled for the K1 endpoint, which may allow network interception of credential or token traffic.

Mitigation: Enable TLS certificate verification and use only trusted K1 endpoints before handling credentials.

Risk: Unsafe credential and token handling may expose accounts or allow local command execution.

Mitigation: Run the login helper only in trusted local environments and update it to remove the PowerShell token interpolation before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuxiaoxin00/skills/k1-kzcloud-skill)
- [Gaode Map LBS skill dependency](https://clawhub.ai/lbs-amap/amap-lbs-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell command examples and tabular response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires K1_KZClOUD_TOKEN and the Gaode Map LBS dependency for location-based lookup.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
