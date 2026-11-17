## Description:

Wraps the Exa MCP server (mcp.exa.ai) for web search, deep research, and related tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-focused agents use this skill to run bounded Exa MCP web search, crawling, company research, code context lookup, and deep research workflows with explicit guardrails for scale and consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, URLs, and research prompts are sent to Exa's external MCP service during normal use.

Mitigation: Avoid submitting confidential data unless external processing by Exa is approved for the deployment environment.

Risk: Long-running deep research tasks can commit significant external resources once started.

Mitigation: Require explicit per-request user confirmation before invoking deep_researcher_start.

Risk: Opaque, shortened, internal, or obfuscated URLs can create SSRF-style exposure when passed to crawling or search tools.

Mitigation: Validate URLs client-side and refuse destinations that cannot be confirmed as appropriate public targets.

Risk: Large crawling or enumeration requests can consume excessive resources or exceed an appropriate research scope.

Mitigation: Scope large jobs into small batches and confirm the purpose before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/mcp-skill-hardened)
- [Exa MCP server](https://mcp.exa.ai/mcp)
- [Faberlens safety evaluation](https://faberlens.ai/explore/mcp-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Plain text or Markdown responses derived from Exa MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal use sends search terms, URLs, and research requests to Exa's external MCP service; deep research requires explicit per-request confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
