## Description: <br>
ShipEngine lets an agent use an OOMOL-connected ShipEngine account to calculate or estimate shipping rates, list carriers, retrieve rates, parse addresses, and validate mailing addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent perform ShipEngine rate, carrier, address parsing, and address validation workflows through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a credentialed OOMOL-connected ShipEngine account for external API activity. <br>
Mitigation: Install only when that account access is acceptable, and review requests that include customer addresses or shipment details before execution. <br>
Risk: Rate, carrier, parsing, and validation requests may affect ShipEngine or OOMOL usage and billing. <br>
Mitigation: Treat connector calls as billable external API activity and pause retries when billing or credit errors are returned. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-shipengine) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [ShipEngine Homepage](https://www.shipengine.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ShipEngine Icon](https://static.oomol.com/logo/third-party/shipengine.png) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns connector results as JSON when actions are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
