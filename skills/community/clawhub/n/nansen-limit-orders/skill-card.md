## Description:

Guide users through native limit orders on Solana via `nansen trade limit-order create|list|cancel|update`, and the alert-based settlement-signal fallback for chains without native support. Use when a user wants a price-triggered buy or sell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, list, update, and cancel price-triggered Solana limit orders. For other chains, it guides users to configure narrowly scoped transfer alerts as best-effort settlement signals for orders placed on a supporting venue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict with medium confidence, but one unresolved reference leaves the scan evidence incomplete.

Mitigation: Review the unresolved reference before installation; the scan guidance says the verdict does not mean the skill is risk-free.

Risk: Creating or cancelling a native limit order submits a real trading action, while transfer alerts are only best-effort settlement signals.

Mitigation: Use `--dry-run` to inspect create or cancel plans and obtain user approval before confirming with `--yes`. Describe alerts as transfer-based settlement signals, not price triggers or authoritative order tracking.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [Nansen CLI on npm](https://www.npmjs.com/package/nansen-cli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands for order management and alert setup, with user-facing explanations of prerequisites and limitations.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
