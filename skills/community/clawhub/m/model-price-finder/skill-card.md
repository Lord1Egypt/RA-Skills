## Description:

Simple tool to fetch and view model pricing from TokenRouter, with optional account registration for extended access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yb98k999](https://clawhub.ai/user/yb98k999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to compare current TokenRouter model pricing and optionally add selected models to their local OpenClaw configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The enable command persistently changes the local OpenClaw model configuration.

Mitigation: Use the list command for read-only price checks, and run enable only when you intend to modify ~/.openclaw/openclaw.json.

Risk: Existing OpenClaw settings can be overwritten if the current configuration cannot be parsed.

Mitigation: Create an independent backup and inspect the planned configuration change before running enable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yb98k999/skills/model-price-finder)
- [PaleBlueDot publisher profile](https://clawhub.ai/user/yb98k999)
- [TokenRouter pricing API](https://www.palebluedot.ai/openIntelligence/api/pricing)
- [PaleBlueDot registration](https://www.palebluedot.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown tables and command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persistently update ~/.openclaw/openclaw.json when the enable command is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
