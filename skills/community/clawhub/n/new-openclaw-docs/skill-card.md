## Description:

Navigate and use OpenClaw documentation efficiently with cached doc fetch/search tooling, sitemap/category routing, and config snippet lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ollieb89](https://clawhub.ai/user/ollieb89)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to answer OpenClaw setup, configuration, troubleshooting, automation, and platform questions with cached documentation search, fetched source pages, and concrete configuration examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cache refresh behavior can remove cached Markdown unexpectedly if the cache directory is misconfigured.

Mitigation: Set OPENCLAW_DOCS_CACHE_DIR to a dedicated cache folder and verify the path before using cache refresh or cleanup commands.

Risk: Copying broad provider or gateway examples can expose agents or services more widely than intended.

Mitigation: Require Discord mentions, scope guild and channel IDs, and bind gateways to localhost unless external access is deliberately protected with authentication and network controls.

Risk: Suggested global installation of qmd can introduce unpinned tooling into the execution environment.

Mitigation: Vet and pin qmd before installation, or keep using the bundled keyword search workflow.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Operations Guide](references/operations.md)
- [Routing Guide](references/routing.md)
- [Common Config Snippets](snippets/common-configs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should cite OpenClaw documentation paths or source URLs when available.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
