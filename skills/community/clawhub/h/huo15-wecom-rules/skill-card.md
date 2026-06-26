## Description: <br>
Provides standardized rules for sending WeCom messages and files through the WeCom API, including fallback behavior, message formatting, and user identity handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide an agent when sending WeCom messages, cards, group notifications, and files while following the publisher's required WeCom API flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exposed WeCom credentials and webhook keys could allow unauthorized API use. <br>
Mitigation: Rotate the exposed secret and webhook key before use, remove hardcoded credentials from the skill, and store replacements in a managed secret store. <br>
Risk: Automatic collection and shared storage of user identity details can expose personal data across users. <br>
Mitigation: Disable automatic profile collection and shared-memory storage unless users receive clear notice and consent controls, access is restricted, and retention rules are defined. <br>
Risk: Gender-based personalization can create avoidable privacy and appropriateness issues. <br>
Mitigation: Remove or disable gender-based forms of address unless there is a clear business need and user-approved profile data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jobzhao15/huo15-wecom-rules) <br>
- [Publisher profile](https://clawhub.ai/user/jobzhao15) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WeCom message and file-sending rules, API request examples, fallback behavior, and user information storage guidance.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
