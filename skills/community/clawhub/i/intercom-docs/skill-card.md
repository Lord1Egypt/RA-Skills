## Description: <br>
Create, update, improve, and review Intercom help-center and support documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgelewi5](https://clawhub.ai/user/georgelewi5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support, product, and documentation teams use this skill to draft, revise, and audit Intercom help-center content. It can also inspect Intercom workspace content through the Intercom API when the user provides a private workspace access token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Intercom workspace access tokens can expose or modify private help-center content if handled carelessly. <br>
Mitigation: Treat tokens as secrets, avoid writing them into docs or files, inspect content read-only first, and review proposed changes before applying them. <br>
Risk: Generated documentation may describe stale, inferred, or unverified product behavior. <br>
Mitigation: Check product behavior, existing docs, code, or support sources before publishing, and clearly mark assumptions or items that need verification. <br>


## Reference(s): <br>
- [Intercom help center collections API endpoint](https://api.intercom.io/help_center/collections) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include review summaries, proposed article bodies, and assumptions to verify.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
