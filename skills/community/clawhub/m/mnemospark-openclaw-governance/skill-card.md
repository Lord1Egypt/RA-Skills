## Description:

Operate OpenClaw multi-agent governance with openclaw-gov for read-only audits, material change documentation, staged discovery, registry and runbook validation, and governance PR shipping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pawlsclick](https://clawhub.ai/user/pawlsclick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and governance maintainers use this skill to audit and maintain OpenClaw governance roots, document material system changes, validate registry and runbook drift, and prepare governance pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on executable third-party code installed from a mutable Git tag.

Mitigation: Review the upstream openclaw-governance source before installing and prefer a full commit SHA or hashed registry release where possible.

Risk: Governance workflows can enable high-impact changes to registry, runbook, CI, and PR processes.

Mitigation: Run with only the repository and GitHub permissions needed for governance work, and keep review gates before mutating or shipping changes.

Risk: Discovery JSON can expose repository remote URLs or unusual embedded credentials.

Mitigation: Share only targeted discovery slices and review outputs for private infrastructure or credential-like values before disclosure.

## Reference(s):

- [OpenClaw Governance repository](https://github.com/pawlsclick/openclaw-governance)
- [Migrating existing governance](https://github.com/pawlsclick/openclaw-governance/blob/main/docs/migrating-existing-governance.md)
- [Brownfield discover flow](references/brownfield-flow.md)
- [openclaw-gov command reference](references/commands.md)
- [Safe discovery JSON slices](references/discovery-json-slices.md)
- [Material change threshold](references/material-change-threshold.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include governance change plans, validation commands, and PR handoff text.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
