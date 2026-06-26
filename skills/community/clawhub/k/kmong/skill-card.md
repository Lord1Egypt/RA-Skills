## Description: <br>
Automates Kmong expert account sign-up, PASS SMS identity verification, profile setup, and initial service registration through an OpenClaw browser workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to guide an OpenClaw browser through Kmong expert onboarding, including sign-up, identity verification, profile setup, and service registration. It is intended for supervised account creation where the user controls identity data and verification codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates real account creation and identity verification with sensitive personal data. <br>
Mitigation: Use it only under close supervision and keep identity fields, SMS codes, CAPTCHA/security characters, and final registration submission under direct user control. <br>
Risk: Local account credentials or profile settings may be stored in a secrets file. <br>
Mitigation: Protect the local secrets file with restrictive permissions and keep it excluded from version control. <br>


## Reference(s): <br>
- [ClawHub Kmong skill page](https://clawhub.ai/mupengi-bot/kmong) <br>
- [Kmong](https://kmong.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with ordered browser-action steps and inline JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires supervised handling of identity fields, CAPTCHA/security characters, SMS codes, Google sign-in, agreements, and final submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
