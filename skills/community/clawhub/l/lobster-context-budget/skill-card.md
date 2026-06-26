## Description: <br>
Audits Claude Code context window consumption across agents, skills, MCP servers, and rules. Identifies bloat, redundant components, and produces prioritized token-savings recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Claude Code context usage across agents, skills, rules, MCP servers, and CLAUDE.md files, then prioritize token-saving cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read workspace instruction and configuration files, including .mcp.json, while estimating context usage. <br>
Mitigation: Review configuration files for secrets or sensitive service details before running the audit. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report with token estimates, component breakdowns, issue rankings, and prioritized recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Verbose mode may include per-file token counts, overlap findings, MCP tool details, and estimated savings.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
