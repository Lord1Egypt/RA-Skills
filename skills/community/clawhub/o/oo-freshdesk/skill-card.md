## Description: <br>
Freshdesk (freshworks.com). Use this skill for Freshdesk requests that search and read data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, support teams, and developers use this skill to read Freshdesk account details, tickets, ticket conversations, and filtered ticket lists through an OOMOL-connected Freshdesk account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Freshdesk account, and ticket or conversation reads can expose customer or business data. <br>
Mitigation: Install and use the skill only when OOMOL is trusted for this account, and review the connected Freshdesk scopes before running read actions. <br>
Risk: The first-time setup path includes a curl-to-shell installer for the oo CLI. <br>
Mitigation: Use the installer only when the oo CLI is not already installed, and prefer the published OOMOL install guide for platform-specific setup. <br>
Risk: Future connector actions may change Freshdesk state if they are tagged as write or destructive. <br>
Mitigation: Fetch the live connector schema before execution and get explicit user confirmation for any write or destructive action payload. <br>


## Reference(s): <br>
- [Freshdesk homepage](https://www.freshworks.com/freshdesk/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub Freshdesk skill page](https://clawhub.ai/oomol/oo-freshdesk) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses schema-first connector actions and may return Freshdesk data in JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
