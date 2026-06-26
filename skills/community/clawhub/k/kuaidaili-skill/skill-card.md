## Description: <br>
Integrates Kuaidaili proxy service workflows so an agent can fetch proxy IPs, check account balance, and test proxy connectivity with user-provided credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw-baixing](https://clawhub.ai/user/openclaw-baixing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Kuaidaili credentials, retrieve private, dedicated, or tunnel proxy IPs, check account balance, and test whether a proxy endpoint works. It is useful when an agent needs scripted access to a paid Kuaidaili proxy account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclaw-baixing/kuaidaili-skill) <br>
- [Kuaidaili API reference](references/api_reference.md) <br>
- [Kuaidaili official site](https://www.kuaidaili.com/) <br>
- [Kuaidaili API documentation](https://www.kuaidaili.com/doc/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown guidance with command examples; scripts return text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Kuaidaili credentials supplied through environment variables or command-line arguments; avoid logging proxy URLs that contain usernames or passwords.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
