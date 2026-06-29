## Description: <br>
为开发者提供代码、方案、Agent Skill 与 MCP Server 的多轴质量和安全审查清单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
开发者、审查者和 Agent 操作者用于在合并 PR、安装 Skill、部署 MCP Server 或提交技术方案前进行质量门控和安全审计。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The review process may require broad repository inspection. <br>
Mitigation: Use it only in workspaces where that review access is intended, and limit the agent context to the files needed for the review. <br>
Risk: Checklist-based findings can be incomplete or misleading if applied without project context. <br>
Mitigation: Validate findings against the code, tests, deployment model, and the author's stated intent before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/mimo-code-review-and-quality) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown review checklist with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review findings, severity labels, verification prompts, and deployment or installation guidance.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
