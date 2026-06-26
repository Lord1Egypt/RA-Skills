## Description: <br>
AI-powered global compliance checker, document generator, and risk assessor for GDPR, CCPA, SOC2, ISO27001, HIPAA and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, compliance teams, and agents use this skill to check documents, generate compliance materials, assess risk, and query requirements across privacy, security, and audit frameworks. Outputs should be reviewed by qualified legal or compliance staff before operational use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary marks the package suspicious because it is advertised as a global compliance skill but also contains separate video-generation instructions. <br>
Mitigation: Review the package before installing and use only the compliance-related files and commands unless the separate video workflow has been deliberately verified. <br>
Risk: The mixed video-generation instructions ask agents to clone external tooling and provide an OpenAI API key. <br>
Mitigation: Do not run the video-generation setup commands, clone the external video repository, or provide API credentials when evaluating or using the compliance skill. <br>
Risk: Compliance outputs may be incomplete or misleading if treated as legal advice or published without review. <br>
Mitigation: Require qualified legal or compliance review before relying on generated policies, audit reports, or risk recommendations. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ZhenStaff/global-compliance) <br>
- [Publisher profile](https://clawhub.ai/user/ZhenStaff) <br>
- [Project link from release changelog](https://github.com/ZhenRobotics/openclaw-global-compliance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-shaped report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce compliance reports, generated policy text, risk assessments, recommendations, and CLI command guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
