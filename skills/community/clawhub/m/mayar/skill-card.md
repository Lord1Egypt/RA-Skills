## Description:

Interact with the Mayar payment platform for invoices, products, payments, customers, transactions, webhooks, QR codes, balance checks, and account identity from an AI agent or shell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayar](https://clawhub.ai/user/mayar)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use this skill to run Mayar CLI workflows for merchant account checks and payment operations. It provides command guidance for listing, creating, closing, reopening, and inspecting payment-related resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned npm package with mayar@latest, so executed CLI behavior may change between runs.

Mitigation: Use a pinned, reviewed Mayar CLI version for production workflows and re-review the skill before changing the pinned version.

Risk: Mayar API keys can grant access to a merchant payment account and may be exposed if passed directly on a command line.

Mitigation: Use least-privilege or revocable API keys, prefer environment or secret-manager injection, and avoid passing secrets through command arguments.

Risk: The documented commands can create, close, reopen, or register payment-related resources.

Mitigation: Require explicit user confirmation before running state-changing payment, invoice, product, customer, or webhook commands.

## Reference(s):

- [Mayar ClawHub Skill Page](https://clawhub.ai/mayar/skills/mayar)
- [Mayar Publisher Profile](https://clawhub.ai/user/mayar)
- [Mayar CLI Homepage](https://github.com/mayarid/mayar-cli)
- [Mayar Dashboard API Key Page](https://web.mayar.id)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI responses may include JSON when commands are run with --json; the skill itself produces guidance and command patterns rather than executing payment operations directly.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter version: 0.1.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
