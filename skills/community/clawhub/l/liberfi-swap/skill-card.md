## Description:

Liberfi Swap helps agents use the LiberFi CLI to list swap chains and tokens, quote swaps, build or broadcast transactions, estimate fees, and present transaction details for explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombmod](https://clawhub.ai/user/bombmod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide token swap workflows and on-chain transaction submission through the LiberFi CLI, including chain and token lookup, quote review, fee estimation, and confirmed transaction broadcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Swap and transaction commands can move funds irreversibly through wallet-linked workflows.

Mitigation: Require token security checks, a clear quote and fee summary, and explicit user confirmation before login, signing, execution, or broadcast.

Risk: The artifact directs silent global CLI installation.

Mitigation: Require explicit approval for installation and prefer a pinned, verified, non-global CLI installation.

Risk: The artifact discourages transparent reporting of package installation failures.

Mitigation: Report installation errors plainly and verify the package source before retrying.

## Reference(s):

- [LiberFi homepage](https://liberfi.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to use structured JSON output; fund-moving actions require token security checks and explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
