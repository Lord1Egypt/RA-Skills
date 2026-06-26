## Description: <br>
A paid-skill template that demonstrates license-key validation for publishing paid skills on ClawHub. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[lintqiu](https://clawhub.ai/user/lintqiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers can use this demo to understand how a ClawHub skill can gate execution on a purchased license key configured through an environment variable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled license check is a basic local example and is not production-grade licensing infrastructure. <br>
Mitigation: Use only a license key intended for this skill, and replace the demo hash check with stronger signed or server-side verification before relying on it in production. <br>
Risk: The skill will fail when SKILL_LICENSE_KEY is missing or invalid. <br>
Mitigation: Configure a dedicated SKILL_LICENSE_KEY for this skill before use and avoid reusing unrelated credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lintqiu/lin-skill-demo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text status messages with JSON-like license-check output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILL_LICENSE_KEY; exits nonzero when the key is missing or invalid.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
