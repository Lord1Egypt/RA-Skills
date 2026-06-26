## Description: <br>
Projitive is an MCP-first governance skill that guides agents through evidence-based project discovery, task context, execution, verification, and task advancement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinxulai](https://clawhub.ai/user/yinxulai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use Projitive to manage repository governance work through Projitive MCP methods, including locating project context, advancing tasks, recording design rationale, and linking completion evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update .projitive governance files in a repository. <br>
Mitigation: Install it only in repositories where Projitive should manage governance state, and review generated governance changes before committing them. <br>
Risk: Task, design, and report files can accidentally capture sensitive project information. <br>
Mitigation: Avoid placing secrets or confidential data in governance task and evidence files. <br>
Risk: The setup flow installs @projitive/mcp@latest, which can change over time. <br>
Mitigation: Separately evaluate or pin the external @projitive/mcp package for controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinxulai/projitive) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and governance workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to create or update .projitive governance files and evidence records.] <br>

## Skill Version(s): <br>
2.1.3 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
