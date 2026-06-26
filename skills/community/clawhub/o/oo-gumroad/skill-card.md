## Description: <br>
Gumroad (gumroad.com). Use this skill for Gumroad requests that read, create, or update data through the OOMOL-connected Gumroad connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a Gumroad account through the oo CLI, including retrieving user, product, sale, subscriber, and sales data and performing supported sale operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected Gumroad account. <br>
Mitigation: Install only when the user is comfortable granting the connector access to that account. <br>
Risk: Refund, shipment update, and receipt resend actions can affect money, fulfillment, or customers. <br>
Mitigation: Require explicit confirmation of the target sale and exact effect before running those actions. <br>
Risk: The first-time setup guidance includes one-line CLI installer commands. <br>
Mitigation: Review the installer source or use a safer installation path before running those commands. <br>


## Reference(s): <br>
- [ClawHub Gumroad skill page](https://clawhub.ai/oomol/oo-gumroad) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Gumroad](https://gumroad.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce oo CLI commands that return JSON connector responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
