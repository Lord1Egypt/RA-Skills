## Description:

Check Mac laptop battery status including percentage, charging state, and time remaining.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airbai](https://clawhub.ai/user/airbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for Mac laptop battery percentage, charging state, and remaining charge or discharge time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is only useful on macOS laptops and may fail or provide no result on other systems.

Mitigation: Use it only for local Mac battery-status questions and fall back to platform-specific battery tools elsewhere.

Risk: The skill executes a local battery-status command, so output depends on pmset availability and current battery telemetry.

Mitigation: Review command output before presenting it and state when battery status cannot be determined.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Concise natural-language status text based on local shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS laptop battery information from pmset; not useful on non-macOS systems or Macs without a battery.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
