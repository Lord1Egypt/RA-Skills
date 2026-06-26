## Description: <br>
Provision and manage Microsoft 365 operated by 21Vianet and Adobe Creative Cloud users, including account creation, license assignment, password reset, deletion, lookup, batch operations, and self-tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT administrators and authorized support agents use this skill to create, license, inspect, reset, and remove Microsoft 365 and Adobe Creative Cloud user accounts during onboarding and account-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles enterprise account administration and sensitive credentials. <br>
Mitigation: Install and run only in a tightly controlled admin environment after code review; rotate any credentials that may have been distributed with the package. <br>
Risk: The HTTP API can expose provisioning, password reset, and deletion actions. <br>
Mitigation: Disable the API unless needed, or place it behind authentication and a trusted network boundary. <br>
Risk: Password reset and notification workflows can disclose initial or reset passwords. <br>
Mitigation: Avoid sending passwords through email or chat and require explicit human confirmation before reset, delete, or self-test actions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/eggyrooch-blip/office-adobe-user-provision) <br>
- [Microsoft 365 operated by 21Vianet portal](https://portal.partner.microsoftonline.cn) <br>
- [Adobe Creative Cloud](https://creativecloud.adobe.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger account-management side effects when an authorized operator runs the generated CLI or HTTP API actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
