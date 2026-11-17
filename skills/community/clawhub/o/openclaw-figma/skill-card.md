## Description:

Enables agents to read Figma design files, inspect components and design tokens, export assets, and use Figma MCP workflows for design-to-code tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyqthu](https://clawhub.ai/user/chenyqthu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and design-system maintainers use this skill to inspect Figma files, generate frontend implementation guidance or code from designs, export visual assets, and coordinate Figma MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may access Figma design data through FIGMA_TOKEN or Figma MCP OAuth.

Mitigation: Use least-privileged credentials, avoid broadly readable environment files, and provide only the Figma files or frames needed for the task.

Risk: Figma MCP write-back workflows can create or modify files when the account has editor access.

Mitigation: Require explicit user approval before any create, modify, or write-back action, then verify changes incrementally.

Risk: Hardcoded Omada asset references may point agents toward design files that are not intended for every audience.

Mitigation: Review the asset registry before distribution and remove or scope links that should not be used in the release context.

## Reference(s):

- [Agent Operation Guide](artifact/references/guide-for-agents.md)
- [Human Workflow Guide](artifact/references/guide-for-humans.md)
- [Omada Figma Asset Registry](artifact/references/omada-assets.md)
- [Figma MCP Server](https://mcp.figma.com/mcp)
- [Figma Personal Access Tokens](https://www.figma.com/settings)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, API output summaries, and generated frontend code where requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on Figma REST API responses, MCP tool responses, exported assets, and user-provided Figma file or frame links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
