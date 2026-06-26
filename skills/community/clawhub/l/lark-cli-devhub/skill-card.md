## Description: <br>
Use when a developer needs lark-cli or feishu-cli workflows to turn Feishu/Lark into a project knowledge hub for bugfix memory, task clarity, release evidence, pitfall lookup, AI run summaries, or main-branch writeback discipline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to operate Feishu/Lark as a project knowledge hub for bugfix memory, task state, release evidence, reusable pitfalls, playbooks, and AI run summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can write project records into a configured Feishu/Lark workspace, which could expose secrets or sensitive project data if misused. <br>
Mitigation: Follow the documented boundary against writing secrets, access tokens, app secrets, private keys, raw credentials, or full environment files. <br>
Risk: Enforced hook mode can block commits or pushes when knowledge writeback evidence is missing. <br>
Mitigation: Start in shadow mode, review the hook policy, and tighten to enforced mode only after the team trusts the workflow. <br>
Risk: Failed Feishu/Lark writes could create a false impression that project knowledge was recorded. <br>
Mitigation: Use outbox items for failed writes, sync them later, and report writeback status in the work summary. <br>


## Reference(s): <br>
- [Domain Map](references/domain-map.md) <br>
- [Hook Policy](references/hook-policy.md) <br>
- [Knowledge Model](references/knowledge-model.md) <br>
- [Search Policy](references/search-policy.md) <br>
- [Writeback Flows](references/writeback-flows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration paths, and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires lark-cli, python3, git, and a configured Feishu/Lark workspace.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
