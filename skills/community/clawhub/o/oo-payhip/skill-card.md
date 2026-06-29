## Description: <br>
Operates Payhip through the OOMOL payhip connector to read, create, update, and delete Payhip data using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Payhip coupons and license keys from an agent session through OOMOL-connected tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables OOMOL-backed tooling to access a user's Payhip account. <br>
Mitigation: Install only when Payhip account access through OOMOL is intended, and keep Payhip connected only for approved workflows. <br>
Risk: Coupon and license actions can change Payhip state. <br>
Mitigation: Review the live action schema and confirm the exact JSON payload and expected effect before running write actions. <br>
Risk: Destructive actions can delete Payhip data. <br>
Mitigation: Require explicit user approval for the target resource before running destructive actions such as coupon deletion. <br>
Risk: Setup commands install or invoke external CLI tooling. <br>
Mitigation: Verify the oo CLI installer source before running setup commands. <br>


## Reference(s): <br>
- [Payhip homepage](https://payhip.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-payhip) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector command output is JSON when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
