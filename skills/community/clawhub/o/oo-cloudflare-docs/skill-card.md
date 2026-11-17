## Description:

Cloudflare Docs (developers.cloudflare.com). Use this skill for any Cloudflare Docs request, including searching and reading documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Cloudflare operators use the skill to search Cloudflare documentation and retrieve information through the OOMOL Cloudflare Docs connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run a remote installer without a separate approval step or integrity checks.

Mitigation: Review the setup and require approval before running an installer; prefer an independently verified, pinned oo CLI release.

Risk: The external installer and hosted connector implementation were not verified.

Mitigation: Use a pinned CLI release from a source you can independently verify, and review the connector setup before connecting an account.

## Reference(s):

- [Cloudflare Developer Documentation](https://developers.cloudflare.com)
- [Cloudflare MCP Server Documentation](https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI Command Reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown guidance and oo CLI commands with JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation answers and command examples for Cloudflare Docs searches and reads.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
