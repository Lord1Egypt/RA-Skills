## Description:

Use when users need to create, query, list, adjust, reduce, or cancel Pionex Futures Grid, Spot Grid, or Smart Copy bot orders, including bulk listing and pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pibrandon](https://clawhub.ai/user/pibrandon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Pionex users use this skill to manage Pionex trading bot lifecycle actions and push trading signals through the Pionex CLI with explicit confirmations for write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live bot create, adjust, reduce, cancel, profit extraction, and signal-publishing actions can affect trading positions or funds.

Mitigation: Use dry runs first, require explicit user confirmation for live actions, and surface Pionex validation errors and constraints before retrying.

Risk: API credentials with broad account permissions could increase the impact of misuse or compromise.

Mitigation: Use a dedicated Pionex API key with only the required bot permissions and avoid withdrawal or unrelated account permissions.

Risk: The npm executable dependency is unpinned in the release evidence.

Mitigation: Pin the npm package version before deployment and review package updates before allowing live trading operations.

Risk: The skill can push trading signals, but the security evidence notes that this capability is not disclosed in the frontmatter description.

Mitigation: Disclose signal publishing in release metadata and confirm every signal-publishing action with the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pibrandon/skills/pionex-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Pionex API credentials, bot permissions, and the pionex-trade-cli executable.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
