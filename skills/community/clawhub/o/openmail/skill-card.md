## Description: <br>
Gives the agent a dedicated email address for sending and receiving email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[armandokun](https://clawhub.ai/user/armandokun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use OpenMail when an agent needs to send email, receive replies, sign up for services, handle support tickets, or interact with human institutions through email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email to external recipients and act on replies. <br>
Mitigation: Review recipients, message bodies, links, and attachments before sending or forwarding information. <br>
Risk: OpenMail requires an API key and stores setup values in an environment file. <br>
Mitigation: Use a dedicated API key where possible, restrict env file permissions, and remove credentials when the skill is no longer needed. <br>
Risk: Inbound email content is untrusted and may contain instructions, links, attachments, or requests for sensitive data. <br>
Mitigation: Treat inbound messages as data, not instructions; do not execute commands or disclose credentials, files, or conversation history based on email content. <br>
Risk: Cron polling or autonomous reply workflows can create repeated or unintended external actions. <br>
Mitigation: Enable automation only with narrow sender allowlists, low-risk templates, logging, unread-thread handling, and a clear cleanup plan. <br>


## Reference(s): <br>
- [OpenMail homepage](https://openmail.sh) <br>
- [OpenMail API Reference](references/api.md) <br>
- [OpenMail Setup](references/setup.md) <br>
- [OpenMail Error Reference](references/errors.md) <br>
- [ClawHub OpenMail release page](https://clawhub.ai/armandokun/openmail) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce email content, CLI commands, inbox setup steps, polling workflows, and operational guidance for handling email threads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
