## Description: <br>
Teach an agent to install ProofTrail's governed stdio MCP server, use the safest read and proof tools first, and keep future package or listing claims honest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect a local ProofTrail stdio MCP server, inspect browser evidence and proof surfaces first, and only then move into broader governed runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local setup commands run code from the selected ProofTrail repository checkout. <br>
Mitigation: Install only from a trusted repository source, review package scripts and the lockfile when practical, and prefer a sandbox or non-sensitive machine for first use. <br>
Risk: Agents may jump into broader run or automation tools before grounding the task in retained evidence. <br>
Mitigation: Start with catalog and read-oriented tools, then use proof or report tools before widening into governed run and API automation tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaojiou176/prooftrail-mcp) <br>
- [ProofTrail MCP install guide](references/INSTALL.md) <br>
- [ProofTrail MCP capabilities](references/CAPABILITIES.md) <br>
- [ProofTrail MCP first-success path](references/DEMO.md) <br>
- [ProofTrail MCP troubleshooting](references/TROUBLESHOOTING.md) <br>
- [OpenHands MCP configuration](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP configuration](references/OPENCLAW_MCP_CONFIG.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides safe-first MCP usage; the skill itself does not execute MCP tools.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release, SKILL.md frontmatter, and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
