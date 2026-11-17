## Description:

Gridman古立特 is a Chinese finance and tax agent skill for audit, accounting, tax, investment banking, compliance, and related workflows, with domain knowledge, execution routing, and review rules.

This skill is for research and development only.

## Publisher:

[zxcharlotte486](https://clawhub.ai/user/zxcharlotte486)

### License/Terms of Use:

CC BY-NC-SA 4.0 for knowledge and Markdown; MIT for scripts

## Use Case:

External finance, audit, tax, accounting, and investment professionals can use this skill for China-focused knowledge questions, workflow-guided task planning, document review, audit workpaper preparation, tax issue analysis, and investment analysis support. Outputs are working aids and must be independently reviewed by qualified professionals before use as formal advice or deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive finance or tax materials may be exposed when optional external integrations, document extraction, browser automation, or private memory are used.

Mitigation: Configure memory and Tools only in user-chosen directories, avoid credentials in Mind, obtain user confirmation before uploads or external writes, and use a dedicated browser profile or sandbox for integrations.

Risk: Optional host tools, MCP servers, npx tooling, MinerU, COM automation, or local CLIs may be unavailable, misconfigured, or unsuitable for the requested workflow.

Mitigation: Verify each optional integration before use and degrade to knowledge guidance when required capabilities are unavailable.

Risk: Finance, audit, tax, legal, or investment outputs could be mistaken for formal professional opinions.

Mitigation: Present outputs as working aids and require independent review by appropriately qualified professionals before formal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxcharlotte486/skills/gridman)
- [README](README.md)
- [Installation and capability setup](INSTALL.md)
- [Routing index](operations/routing_index.md)
- [Execution and review flow](operations/routing_flow.md)
- [Capability registry](operations/capability_registry.md)
- [Source directory](operations/source_directory.md)
- [Workflow guide](references/workflows/README.md)
- [MinerU API documentation](https://mineru.net/apiManage/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional code blocks, shell commands, configuration snippets, and generated files when host tools are available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user authorization before uploads, external writes, destructive actions, or use of private tools; outputs require professional review.]

## Skill Version(s):

3.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
