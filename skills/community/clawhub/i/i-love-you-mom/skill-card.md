## Description: <br>
Automates a monthly photo-to-Mixtiles workflow by collecting photos from a WhatsApp group, curating selected images with vision, building a multi-photo Mixtiles cart link, and sending it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SaharCarmel](https://clawhub.ai/user/SaharCarmel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users or agents use this skill to prepare a recurring family photo tile order by collecting recent WhatsApp group images, selecting suitable photos, creating a Mixtiles cart link, and sending that link to the configured recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private WhatsApp group photos. <br>
Mitigation: Grant access only to the intended group and set MIXTILES_GROUP_JID narrowly before execution. <br>
Risk: Selected family photos may leave local or WhatsApp storage during the Mixtiles and Cloudinary cart flow. <br>
Mitigation: Review the dependent Mixtiles cart script and require manual confirmation before any upload. <br>
Risk: The skill can send a generated cart link without a clear review step. <br>
Mitigation: Add a manual approval step before sending and verify MIXTILES_SEND_TO points to the intended recipient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SaharCarmel/i-love-you-mom) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON manifest output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires wacli, jq, python3, WhatsApp group access, and a dependent Mixtiles cart script.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
