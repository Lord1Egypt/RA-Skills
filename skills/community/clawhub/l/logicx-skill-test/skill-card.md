## Description: <br>
Call LogicX frontend proxy APIs for health checks, browser binding, password login, user info, orders, payments, and account actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QihangYang](https://clawhub.ai/user/QihangYang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to connect to LogicX, verify account state, review orders, and perform confirmed account or payment actions through the LogicX frontend proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags account API access and credential handling as suspicious. <br>
Mitigation: Install only if the LogicX service and QihangYang publisher are trusted, and review the skill before use. <br>
Risk: Password login can expose user credentials to the agent conversation. <br>
Mitigation: Prefer browser binding and do not send passwords in chat unless the user explicitly accepts that fallback. <br>
Risk: The default service endpoint is a plain-HTTP IP address. <br>
Mitigation: Avoid using the default plain-HTTP endpoint for real accounts or payments. <br>
Risk: The skill stores LogicX authorization state on the local machine. <br>
Mitigation: Remove ~/.config/logicx/skill-state.json or unlink the agent when access should no longer persist. <br>


## Reference(s): <br>
- [LogicX skill page](https://clawhub.ai/QihangYang/logicx-skill-test) <br>
- [Publisher profile](https://clawhub.ai/user/QihangYang) <br>
- [API reference](references/api-reference.md) <br>
- [Example dialogues](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or summarize LogicX account, order, payment, and authorization API responses.] <br>

## Skill Version(s): <br>
0.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
