## Description: <br>
飞书审批 API：审批实例、审批任务管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gu2003li](https://clawhub.ai/user/gu2003li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Lark Approval schemas, query approval instances and tasks, and perform approval actions through lark-cli when their Lark credentials allow it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform approval workflow actions when the user's Lark credentials include approval write scopes. <br>
Mitigation: Install only for agents that should operate Lark Approval workflows, and review requested approval scopes before use. <br>
Risk: Incorrect data or parameter shapes could affect real approval instances or tasks. <br>
Mitigation: Run the documented schema command before API calls and review command inputs before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gu2003li/lark-approval) <br>
- [Publisher profile](https://clawhub.ai/user/gu2003li) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with inline shell commands and CLI method names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires lark-cli and appropriate Lark approval scopes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
