## Description: <br>
Teach an agent to install Movi's local MCP server, stay review-first, and use the safest manifest and batch-analysis tools before deeper mutation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to attach a local Movi MCP server and inspect jobs, review queues, and manifests before authorizing heavier batch changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP configuration uses a local path placeholder and could launch an unintended checkout if replaced carelessly. <br>
Mitigation: Replace the placeholder only with a trusted Movi checkout and review the repository and dependencies before starting the MCP server. <br>
Risk: Patch and rule-apply tools can mutate manifests or review rules. <br>
Mitigation: Start with jobs.list, review_queue.get, manifest.get, and analyze.create, and require explicit operator approval before manifest.patch_row, manifest.batch_patch, review_rule.apply, or similar mutation actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaojiou176/movi-review-first-bundle) <br>
- [Install And Attach Movi MCP](references/INSTALL.md) <br>
- [Movi MCP Capabilities](references/CAPABILITIES.md) <br>
- [First-Success Path](references/DEMO.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [OpenHands MCP configuration](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP configuration](references/OPENCLAW_MCP_CONFIG.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs emphasize review-first inspection and require explicit user approval before mutation tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
