## Description:

Secrets management for AI agents. Never expose your API keys again.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsdouglas](https://clawhub.ai/user/rsdouglas)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Janee to give MCP-compatible agents controlled access to external APIs while keeping API credentials encrypted locally, enforcing request policies, and maintaining audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A compromised or prompt-injected agent could trigger the reported URL-handling flaw and send stored credentials to an attacker-controlled URL.

Mitigation: Before high-trust use, require rejection of absolute and protocol-relative paths, validate the final request origin before adding credentials, and require HTTPS except for explicit local development.

Risk: Production or high-privilege API keys carry elevated impact if Janee is installed before the reported security guidance is addressed.

Mitigation: Review before installing with production keys, use least-privilege credentials, encrypt all credential-bearing fields, and update flagged dependencies.

## Reference(s):

- [Janee ClawHub Skill Page](https://clawhub.ai/rsdouglas/skills/janee)
- [Janee README](artifact/README.md)
- [Path-Based Request Policies](artifact/docs/POLICIES.md)
- [Janee Changelog](artifact/docs/CHANGELOG.md)
- [Janee npm Package](https://www.npmjs.com/package/@true-and-useful/janee)
- [Janee OpenClaw Plugin npm Package](https://www.npmjs.com/package/@true-and-useful/janee-openclaw)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, YAML and JSON configuration examples, and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, MCP tool usage, and local Janee configuration paths.]

## Skill Version(s):

0.1.2 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
