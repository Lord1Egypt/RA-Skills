## Description: <br>
A-Leads helps an agent search and read A-Leads data for business email discovery, personal email discovery, phone lookup, and email verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent query A-Leads through an OOMOL-connected account for lead enrichment, contact discovery, and email deliverability checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can look up business emails, personal emails, phone numbers, and email verification signals, which may involve sensitive contact data. <br>
Mitigation: Use it for explicit user-requested contact lookups and review the requested target and payload before execution. <br>
Risk: The skill depends on the local oo CLI and an OOMOL-connected A-Leads account. <br>
Mitigation: Install and connect OOMOL only when needed, verify the account and provider connection, and resolve billing or credential errors before retrying. <br>


## Reference(s): <br>
- [A-Leads homepage](https://a-leads.co) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs live schema checks before constructing connector payloads and returns connector JSON responses when actions are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
