## Description: <br>
EmailListVerify helps agents verify email addresses, check disposable domains, manage batch email-list verification, and retrieve verification credits through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operations teams use this skill to verify individual email addresses, assess disposable domains, and manage EmailListVerify batch list checks from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected EmailListVerify account and sensitive credentials managed through OOMOL. <br>
Mitigation: Grant access only to the intended OOMOL and EmailListVerify connection, and review requested account scopes before use. <br>
Risk: Batch upload and list deletion actions can change or remove EmailListVerify data. <br>
Mitigation: Confirm exact payloads, list identifiers, and intended effects with the user before running write or destructive actions. <br>
Risk: The security conclusion is based on clean scanner telemetry and the visible artifact evidence. <br>
Mitigation: Review the installed skill text and connector behavior before deployment, especially for credential, external service, or write-action changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-emaillistverify) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [EmailListVerify Homepage](https://emaillistverify.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return EmailListVerify connector responses as JSON when actions are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
