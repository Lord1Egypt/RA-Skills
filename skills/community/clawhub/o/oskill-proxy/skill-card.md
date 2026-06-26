## Description: <br>
Oskill Proxy guides an agent to use a local Android HTTP proxy to start activities and services, send broadcasts, and operate ContentProviders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SOSO-eng](https://clawhub.ai/user/SOSO-eng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill when they need to invoke Android components through a local OSkillProxy service, including from environments such as Termux where direct Intent or component calls are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad Android component and ContentProvider operations through a local proxy, including actions that can query sensitive providers or modify and delete provider data. <br>
Mitigation: Use it only with a trusted OSkillProxy Android app, keep the service bound to localhost, and require explicit approval before invoking unknown components or changing ContentProvider data. <br>
Risk: The artifact includes a concrete-looking bearer token in configuration. <br>
Mitigation: Replace and rotate the token before use and avoid treating the bundled token as a production secret. <br>


## Reference(s): <br>
- [OSkill Proxy Skill Source](artifact/SKILL.md) <br>
- [ClawHub Release Page](https://clawhub.ai/SOSO-eng/oskill-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local OSkillProxy Android app, a bearer token, and a localhost HTTP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
