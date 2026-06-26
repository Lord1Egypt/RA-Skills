## Description: <br>
Send beautifully formatted HTML emails via gog CLI with templates and styling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[syedair](https://clawhub.ai/user/syedair) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other gog CLI users use this skill to prepare styled HTML email bodies from reusable templates, replace placeholders, and send them through configured Gmail tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prepares and sends email through configured Gmail tooling, so mistakes in recipients, subjects, links, attachments, or generated HTML can be sent externally. <br>
Mitigation: Review the rendered HTML, recipient list, subject, links, and attachments before sending, and test important messages by sending them to yourself first. <br>
Risk: Email bodies can expose sensitive information if secrets or confidential data are inserted into placeholders. <br>
Mitigation: Avoid placing secrets or sensitive data in generated email content and remove any accidental sensitive values before sending. <br>
Risk: Editing bundled templates directly can affect future messages that reuse the same template. <br>
Mitigation: Save customized templates as user-specific copies when changes should not affect future runs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/syedair/gog-html-email) <br>
- [Publisher profile](https://clawhub.ai/user/syedair) <br>
- [gog CLI homepage](https://gogcli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and HTML email templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog CLI and a configured Gmail sending environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
