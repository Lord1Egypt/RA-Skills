## Description: <br>
Collective immunity network for AI agents that detects prompt injection patterns, supports community validation, and distributes threat intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seojoonkim](https://clawhub.ai/user/seojoonkim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use HiveFence to add prompt injection detection and community-updated threat intelligence to AI agent workflows. It is intended for environments where prompts can be screened before agent execution and derived threat data may be reported to a third-party service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically reports derived threat data to a third-party service. <br>
Mitigation: Review what data is sent, confirm whether reporting can be disabled, and avoid use with private, regulated, or proprietary prompts until the publisher documents the reporting behavior. <br>
Risk: The supplied artifacts reference an external npm package whose behavior is not visible in the release evidence. <br>
Mitigation: Audit the npm package and its dependencies before installation, and pin reviewed versions in production environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seojoonkim/hivefence) <br>
- [HiveFence Website](https://hivefence.com) <br>
- [HiveFence API Docs](https://hivefence.com/docs) <br>
- [HiveFence GitHub Repository](https://github.com/seojoonkim/hivefence) <br>
- [VittoStack Security Guide](https://x.com/vittostack/status/2018326025373900881) <br>
- [ZeroLeaks Security Assessment](https://x.com/NotLucknite/status/2017665998514475350) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose API calls to a third-party threat reporting and pattern update service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
