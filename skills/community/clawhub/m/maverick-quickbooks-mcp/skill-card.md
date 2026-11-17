## Description:

Provides QuickBooks integration context for customers, invoices, payments, expenses, vendors, and financial reports after Maverick connects QuickBooks and provisions runtime OAuth credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect QuickBooks accounting data, prepare invoice and expense workflows, and summarize financial reports through available runtime tools. Operators should confirm user intent before any write-capable accounting action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QuickBooks OAuth credentials are stored locally for mcporter and could expose accounting data if the account or credentials file is mishandled.

Mitigation: Run under a least-privileged account and ensure ~/.mcporter/credentials.json is readable only by the owning user.

Risk: The install path uses the mcporter package without a pinned version, which can introduce supply-chain changes over time.

Mitigation: Pin mcporter to a reviewed version where possible and install only when Maverick and the package path are trusted.

Risk: Write-capable QuickBooks operations can create, update, delete, send, void, or sync records that affect financial books.

Mitigation: Confirm clear user intent and read the current object state before any money-moving or accounting-affecting change.

Risk: The artifact does not include a provider-owned QuickBooks MCP manifest, so the wrapper is not ready to invoke a local manifest by itself.

Mitigation: Inspect available QuickBooks runtime tools first and do not invoke the wrapper until a provider MCP manifest is added.

## Reference(s):

- [QuickBooks ClawHub skill page](https://clawhub.ai/maverick/skills/maverick-quickbooks-mcp)
- [mcporter](https://github.com/steipete/mcporter)
- [jq](https://stedolan.github.io/jq/)
- [util-linux](https://github.com/util-linux/util-linux)
- [Digest::SHA](https://metacpan.org/pod/Digest::SHA)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Maverick-provisioned QuickBooks OAuth environment variables and available runtime QuickBooks tools.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
