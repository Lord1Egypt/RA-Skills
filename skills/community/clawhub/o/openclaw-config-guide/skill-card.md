## Description:

Guides agents and developers through safe OpenClaw configuration changes, including reading current settings, applying incremental patches, verifying results, and avoiding common path mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacktian010105](https://clawhub.ai/user/jacktian010105)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents use this skill when modifying OpenClaw configuration, adding providers or channels, resolving configuration errors, or checking correct config paths before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reading complete OpenClaw configuration can expose API keys, bot tokens, and gateway tokens.

Mitigation: Prefer scoped configuration reads when possible, redact secrets from outputs, and treat any full configuration output as sensitive.

Risk: Configuration patches can unintentionally change credentials, providers, channels, or gateway behavior.

Mitigation: Review and confirm each patch before applying it, then verify the resulting configuration.

## Reference(s):

- [OpenClaw configuration path quick reference](references/common-paths.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples and configuration path examples for OpenClaw.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
