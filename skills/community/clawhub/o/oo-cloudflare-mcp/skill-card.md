## Description:

Use Cloudflare MCP through an OOMOL-connected account to read, create, and update Cloudflare data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search Cloudflare documentation and inspect Cloudflare API endpoints, then perform Cloudflare MCP actions through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup uses a remote installer whose downloaded code is unverified.

Mitigation: Review setup before enabling the skill and install a reviewed oo CLI release yourself.

Risk: The CLI may install or refresh additional agent skills without explaining those changes.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if you do not want additional skills installed or refreshed.

Risk: Cloudflare actions can change account state.

Mitigation: Use narrowly scoped Cloudflare credentials and retain the skill's required confirmation step for changes.

## Reference(s):

- [Cloudflare MCP](https://github.com/cloudflare/mcp)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON connector results, plus Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
