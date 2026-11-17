## Description:

Control LG smart appliances via ThinQ API. Use when user asks about their fridge, washer, dryer, AC, or other LG appliances. Supports checking status, changing temperature, toggling modes (express, eco), and monitoring door status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiofreitas](https://clawhub.ai/user/kaiofreitas)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect and control LG ThinQ-connected appliances, including refrigerators, washers, dryers, and air conditioners. It supports device listing, status checks, refrigerator temperature changes, mode toggles, and limited washer or dryer monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The raw command can send arbitrary authenticated control payloads to connected appliances.

Mitigation: Avoid the raw command unless the payload and device impact are understood; prefer bounded commands that validate state-changing inputs.

Risk: The skill requires a ThinQ personal access token for appliance control.

Mitigation: Use a dedicated or least-privileged token if available and store it with restrictive file permissions.

## Reference(s):

- [ClawHub LG ThinQ Skill Page](https://clawhub.ai/kaiofreitas/skills/lg-thinq)
- [LG ThinQ Personal Access Token Portal](https://connect-pat.lgthinq.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return appliance status text or JSON-like device status data depending on the command.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
