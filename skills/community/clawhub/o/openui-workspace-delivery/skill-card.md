## Description: <br>
Teach an agent how to install OpenUI MCP Studio, connect it to a host, and use the core UI generation and review workflow without overclaiming a live marketplace listing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to attach a local OpenUI MCP Studio server to compatible agent hosts, generate or review shadcn-style UI changes, and run a local proof loop before making public claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides installation of an external Node project and local dependencies. <br>
Mitigation: Review the external repository and dependencies before installation, and start in a non-sensitive test workspace. <br>
Risk: Host configuration requires a Gemini API key. <br>
Mitigation: Provide the key only through local host configuration or environment handling, and avoid committing a real GEMINI_API_KEY. <br>
Risk: Generated UI diffs or file-apply workflows may modify a workspace. <br>
Mitigation: Inspect generated diffs and quality-gate output before allowing apply or shipping-style tools to make changes. <br>


## Reference(s): <br>
- [OpenUI Workspace Delivery Skill](artifact/SKILL.md) <br>
- [Install And Attach OpenUI MCP Studio](artifact/references/INSTALL.md) <br>
- [OpenUI MCP Studio Capabilities](artifact/references/CAPABILITIES.md) <br>
- [OpenUI MCP Studio First-Success Demo](artifact/references/DEMO.md) <br>
- [OpenUI MCP Studio Troubleshooting](artifact/references/TROUBLESHOOTING.md) <br>
- [OpenHands MCP Config](artifact/references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP Config](artifact/references/OPENCLAW_MCP_CONFIG.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaojiou176/openui-workspace-delivery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is scoped to local MCP setup, UI generation, review bundles, and proof-loop evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
