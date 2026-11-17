## Description:

Fetch raw JSON listing payloads from Paragon MLS for debugging parser behavior, inspecting source payloads, or custom downstream analysis on unprocessed listing data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earlvanze](https://clawhub.ai/user/earlvanze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to call the Paragon MLS raw listings tool when they need original listing JSON instead of normalized parser output. It supports parser debugging, MLS region payload comparison, and custom downstream analysis on unprocessed listing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime and build behavior depend on mutable files outside the packaged skill.

Mitigation: Review and trust the external Paragon MLS MCP project before installation; prefer a package that includes source, lockfile, build output, or a digest-pinned executable.

Risk: Raw MLS payload structure can vary across regions and may be less stable than normalized parser output.

Mitigation: Validate downstream logic against the target MLS regions and use this skill primarily for inspection, debugging, and controlled custom processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earlvanze/skills/paragon-mls-raw-listings)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with MCP command examples; the MCP tool returns raw JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Raw listing payload structure can vary across MLS regions]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
