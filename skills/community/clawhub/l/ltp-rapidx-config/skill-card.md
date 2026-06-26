## Description: <br>
Use when an agent needs to install or configure RapidX CLI/MCP access, set production LTP credentials, locate the agent workspace MCP config, review integration, discover tools, or run read-only self-checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquiditytech](https://clawhub.ai/user/liquiditytech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure RapidX CLI or MCP access in an agent workspace, handle required LTP credentials, verify tool availability, and run read-only setup checks before market or trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow handles LTP credentials and may update an agent workspace MCP configuration. <br>
Mitigation: Use chat-secret or secret-manager flows where available, keep credentials masked, and review MCP configuration changes before accepting them. <br>
Risk: A configured RapidX MCP server can expose trading-capable tools even though this setup skill emphasizes read-only verification. <br>
Mitigation: Limit setup validation to read-only checks, confirm the runtime status before use, and require explicit user authorization before any trading workflow. <br>


## Reference(s): <br>
- [RapidX Capability Overview](references/capability-overview.md) <br>
- [RapidX Skills / CLI / MCP Best Practices](references/best-practices.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/liquiditytech/ltp-rapidx-config) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown with inline bash, JSON, and review-table snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include masked credential references and read-only verification evidence.] <br>

## Skill Version(s): <br>
1.0.14 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
