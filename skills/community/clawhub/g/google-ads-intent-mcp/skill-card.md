## Description:

Analyze Google Ads search-term CSV exports locally and draft negative-keyword plans with dry-run safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, advertisers, and agent operators use this skill to install, configure, and safely run Google Ads Intent MCP for local search-term CSV analysis and negative-keyword planning. It also guides privacy checks, dry-run review, and troubleshooting for MCP-compatible clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions install mutable remote code from a Git URL without pinning a reviewed version.

Mitigation: Review the upstream repository, prefer a pinned commit or trusted versioned release, and run setup in a low-privilege environment.

Risk: Advertising exports and credentials such as OAuth tokens, API keys, service-account JSON, or local token files could be exposed during setup or troubleshooting.

Mitigation: Run diagnostics without secrets or unrelated credentials present, avoid printing private data, and keep user consent explicit before inspecting local files.

Risk: Negative-keyword recommendations or future live-mode tooling could affect advertising performance if applied without review.

Mitigation: Default to exported CSV analysis and dry-run plans, and require explicit confirmation before any live provider call or account mutation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davidmosiah/skills/google-ads-intent-mcp)
- [Repository](https://github.com/davidmosiah/google-ads-intent-mcp)
- [Docs/site](https://github.com/davidmosiah/google-ads-intent-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes local CSV analysis, dry-run planning, privacy checks, and explicit consent before any future live account mutation.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
