## Description:

Real-time retrieval of the latest official OpenClaw documentation, returned as compact LLM-friendly Markdown for config, CLI, channels, gateway, and skills questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakayoo](https://clawhub.ai/user/sakayoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, and agent builders use this skill to answer OpenClaw setup, configuration, CLI, gateway, channels, diagnostics, deployment, and skills questions from current official documentation instead of stale model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation search terms are sent to Mintlify/OpenClaw documentation services.

Mitigation: Avoid secrets, private hostnames, customer names, and internal incident details in search queries.

Risk: Dependency hygiene risk may remain in the JavaScript package dependencies.

Mitigation: Update dependencies and re-run security review before production deployment.

Risk: Poor search terms can return weak or incomplete documentation results.

Mitigation: Prefer English keywords, inspect the returned source path, and fetch the specific page before using guidance for configuration or operational changes.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw Documentation Search Endpoint](https://leaves.mintlify.com/api/search/clawdhub)
- [ClawHub Skill Page](https://clawhub.ai/sakayoo/skills/openclaw-docs-search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Compact Markdown search results or single-page documentation extracts with source paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output removes noisy metadata and detail output extracts only the page content area.]

## Skill Version(s):

1.0.4 (source: server release evidence, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
