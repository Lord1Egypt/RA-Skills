## Description: <br>
Gridman is a finance and tax assistant that routes accounting, audit, tax, investment banking, internal control, ESG, and related questions to a large Markdown knowledge base and optional MCP tools. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zxcharlotte486](https://clawhub.ai/user/zxcharlotte486) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, tax, accounting, audit, and investment users use this skill for professional knowledge guidance, workflow planning, document drafting, and analysis support. With the optional MCP tool layer installed, agents can also propose or run calculations, file-producing workflows, OCR, market-data lookups, and configuration steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer instructions ask an agent to install software, execute shell commands, and edit persistent MCP configuration. <br>
Mitigation: Do not run INSTALL.md automatically; review each command, verify the wheel or package source, and manually approve MCP configuration changes. <br>
Risk: OCR, market data, and memory features can involve tokens, uploaded files, and sensitive financial or business context. <br>
Mitigation: Treat uploaded files, credentials, and gridman-mind outputs as sensitive; avoid unnecessary persistence and redact or restrict access before analysis. <br>
Risk: The skill provides audit, tax, legal, and finance guidance that could be mistaken for formal professional advice. <br>
Mitigation: Require qualified professional review before relying on outputs for filings, audit opinions, legal positions, investment decisions, or other regulated decisions. <br>
Risk: The security verdict is suspicious because runtime instructions grant broad authority to install tools, write configuration, and store business context. <br>
Mitigation: Deploy in a reviewed environment with explicit user approval gates for command execution, configuration edits, credential use, and file writes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxcharlotte486/gridman) <br>
- [README](artifact/README.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [Agent adaptation guide](artifact/AI适配引导.md) <br>
- [End-to-end workflows](artifact/references/workflows.md) <br>
- [Accounting standards knowledge base](artifact/references/accounting_core.md) <br>
- [Audit standards and practice](artifact/references/audit.md) <br>
- [Tax law knowledge base](artifact/references/tax_core.md) <br>
- [MaoDocs accounting and auditing references](https://docs.maoyanqing.com/) <br>
- [nigo-skills reference project](https://github.com/nigo81/nigo-skills) <br>
- [tools-for-auditor reference project](https://github.com/nigo81/tools-for-auditor) <br>
- [Anthropic financial-services cookbook reference](https://github.com/anthropics/anthropic-cookbook) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown, text, code blocks, shell commands, configuration snippets, and optional generated files from MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Knowledge-only use produces guidance from Markdown references; optional MCP use may create files under a runtime memory/output directory and may require user-provided credentials.] <br>

## Skill Version(s): <br>
1.9.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
