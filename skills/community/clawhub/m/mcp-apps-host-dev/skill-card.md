## Description:

Use when developing or debugging the MCP Apps host layer in any agent application - rendering sandboxed iframe cards, bridging postMessage to gateway to MCP server, or fixing security and architectural issues in the card pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oriliz](https://clawhub.ai/user/oriliz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement, debug, and review MCP Apps host behavior in agent applications, including sandboxed card rendering, message bridging, security gates, CSP handling, cache behavior, and common host-side failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated host changes may leave card-originated model turns under-authorized.

Mitigation: Require explicit authorization for card-originated model turns and separate card data from user instructions.

Risk: Broad bridge permissions may let untrusted cards invoke capabilities beyond the card's intended scope.

Mitigation: Use per-card or per-tool allowlists and audit card-originated requests before forwarding them to MCP execution.

Risk: Overly broad CSP and form permissions can increase exposure from untrusted card content.

Mitigation: Restrict CSP domains and form actions to the minimum domains required by each card.

Risk: Durable browser storage may retain sensitive card payloads longer than intended.

Mitigation: Avoid durable localStorage for sensitive payloads, clear card caches promptly, and prefer reviewed installation paths.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/oriliz/mcp-apps-host-dev)
- [ClawHub skill page](https://clawhub.ai/oriliz/skills/mcp-apps-host-dev)
- [Hermes Agent reference implementation](https://github.com/NousResearch/hermes)
- [DeepSeek Harness reference implementation](https://github.com/deepseek-ai/deepseek-harness)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces host-side implementation and debugging guidance; does not itself execute MCP Apps host changes.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
