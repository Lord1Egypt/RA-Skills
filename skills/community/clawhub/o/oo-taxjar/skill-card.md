## Description: <br>
Helps an agent inspect TaxJar connector schemas and run TaxJar read, write, and delete actions through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to calculate sales tax, retrieve rates, validate VAT IDs, and manage TaxJar customers, orders, and refunds from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a user's TaxJar account through OOMOL and requires sensitive account credentials to be connected. <br>
Mitigation: Install it only when TaxJar account access is intended, and keep account connection and credential handling within the OOMOL setup flow. <br>
Risk: Customer, order, refund, update, and delete actions can affect business tax records. <br>
Mitigation: Review the exact payload, target record, and expected effect with the user before approving write or destructive actions. <br>
Risk: TaxJar action inputs can change or differ by account configuration. <br>
Mitigation: Fetch the live connector schema before building each action payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-taxjar) <br>
- [TaxJar homepage](https://www.taxjar.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON payload or response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated oo CLI plus a connected TaxJar account; write and delete actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
