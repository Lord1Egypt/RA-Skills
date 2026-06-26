## Description: <br>
Routes tasks between GLM-4.7-FlashX for simple queries and GLM-5 for coding, analysis, reasoning, and complex tasks, switching automatically as needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raufimusaddiq](https://clawhub.ai/user/raufimusaddiq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use GLM Autoroute to route lightweight prompts to GLM-4.7 and delegate coding, analysis, research, planning, and other complex work to GLM-5. The skill also guides GLM-5 sub-agents to return concise task summaries for code work while saving full code to files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and context may be forwarded to a delegated GLM-5 session. <br>
Mitigation: Avoid including secrets or sensitive data in prompts that may be delegated. <br>
Risk: Delegated work may create local MEMORY.md, research, report, or code files. <br>
Mitigation: Review created file paths and contents before relying on them or sharing them. <br>
Risk: Generated code may be saved to files for later use. <br>
Mitigation: Inspect and test generated code before running it in a trusted environment. <br>


## Reference(s): <br>
- [GLM Autoroute ClawHub release page](https://clawhub.ai/raufimusaddiq/glm-autoroute) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with sessions_spawn command examples and file-writing rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct delegated GLM-5 sessions to save code in files, create research or analysis reports, and update MEMORY.md with key insights.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
