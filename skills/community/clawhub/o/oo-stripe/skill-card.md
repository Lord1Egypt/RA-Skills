## Description: <br>
Operate Stripe through an OOMOL-connected account for reading, creating, updating, and deleting Stripe data instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to operate Stripe through an OOMOL-connected account, including customer, product, and price workflows for read, create, update, search, and delete tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Create, update, and delete actions can affect real Stripe customers, products, prices, and business records. <br>
Mitigation: Review the exact payload, target, and intended effect before approving any write or destructive command. <br>
Risk: The skill operates a connected Stripe account through OOMOL with sensitive credentials. <br>
Mitigation: Install it only where agent operation of the connected Stripe account is acceptable, and inspect the live action schema before executing connector actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-stripe) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Stripe](https://stripe.com) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call the OOMOL oo CLI and return connector responses with data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
