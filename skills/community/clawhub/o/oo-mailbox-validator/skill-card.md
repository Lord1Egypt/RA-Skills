## Description: <br>
MailboxValidator helps agents validate email deliverability and check disposable or free email status through an OOMOL-connected MailboxValidator account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to validate a single email address and check whether it belongs to a disposable or free provider through MailboxValidator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email addresses are personal data sent through OOMOL to MailboxValidator for validation. <br>
Mitigation: Submit only email addresses the user is authorized to process, and follow applicable privacy and data-handling requirements. <br>
Risk: The skill requires an OOMOL-connected MailboxValidator account and may require first-time CLI installation or account connection. <br>
Mitigation: Review first-time installation, sign-in, and connection steps before allowing them, and do not expose raw credentials or API tokens. <br>


## Reference(s): <br>
- [MailboxValidator homepage](https://www.mailboxvalidator.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MailboxValidator connector output in JSON when actions are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence metadata and release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
