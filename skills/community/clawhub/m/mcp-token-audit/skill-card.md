## Description: <br>
Analyze your MCP server config to estimate token consumption per tool. Identify which tools are blowing up your context window, get per-role groupings to keep subagents under the limit, and generate optimized role-specific MCP configs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhinas90](https://clawhub.ai/user/abhinas90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit MCP configuration token footprint, identify high-cost tools, and plan smaller role-specific MCP setups for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token estimates and role groupings are approximate and may not match the exact tokenizer or runtime behavior of every agent environment. <br>
Mitigation: Review the audit results and test revised MCP configurations before relying on them in production workflows. <br>
Risk: The auditor reads local MCP configuration files and its report may reveal server names, tool names, and workflow structure. <br>
Mitigation: Run it only against intended config paths and review reports before sharing them outside the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhinas90/mcp-token-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Human-readable audit report or JSON summary with token estimates, role groupings, and optimization suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the selected report format to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
