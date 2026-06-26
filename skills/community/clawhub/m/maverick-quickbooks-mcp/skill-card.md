## Description: <br>
Use QuickBooks integration context for customers, invoices, payments, expenses, vendors, and financial reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external agents use this skill to inspect QuickBooks accounting data, create invoices, review expenses, and summarize financial reports after Maverick provisions OAuth credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QuickBooks OAuth tokens can grant sensitive accounting access and are stored in a shared local mcporter vault. <br>
Mitigation: Install only for intended QuickBooks access, restrict permissions on ~/.mcporter/credentials.json, and re-authorize if the OAuth grant is revoked. <br>
Risk: Create, update, delete, send, void, or sync actions can make real accounting changes. <br>
Mitigation: Confirm explicit user intent and read current object state before any write or money-moving operation. <br>
Risk: Runtime tool boundaries are unclear because no provider-owned QuickBooks MCP manifest is included in the artifact. <br>
Mitigation: Confirm the actual MCP endpoint, OAuth scopes, and available tool schemas before use; use the smallest read path needed for the task. <br>
Risk: The mcporter dependency is installed without a pinned package version by the artifact metadata. <br>
Mitigation: Pin mcporter to an approved version when supply-chain control matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-quickbooks-mcp) <br>
- [mcporter](https://github.com/steipete/mcporter) <br>
- [jq](https://stedolan.github.io/jq/) <br>
- [util-linux flock](https://github.com/util-linux/util-linux) <br>
- [Digest::SHA](https://metacpan.org/pod/Digest::SHA) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and runtime tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Maverick-provisioned QuickBooks OAuth credentials and available runtime QuickBooks tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
