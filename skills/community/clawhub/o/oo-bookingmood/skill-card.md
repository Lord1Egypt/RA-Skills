## Description: <br>
Bookingmood helps an agent read Bookingmood bookings, products, and product availability through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Bookingmood booking, product, and availability data from their connected Bookingmood account through the OOMOL oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may access Bookingmood bookings, products, and availability from the connected account when a request is broad or ambiguous. <br>
Mitigation: Use the skill for explicit Bookingmood data requests and review requested fields before running connector actions. <br>
Risk: First-time use requires installing the oo CLI and connecting a Bookingmood account through OOMOL. <br>
Mitigation: Review the oo CLI installation and OOMOL connection steps before first use, and connect only the intended Bookingmood account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-bookingmood) <br>
- [Bookingmood Homepage](https://www.bookingmood.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live Bookingmood connector schema before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
