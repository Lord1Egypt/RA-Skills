## Description:

Operate Cloudflare Browser Run through a connected OOMOL account to render pages and extract HTML, JSON, Markdown, links, or selected elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to render web pages with Cloudflare Browser Run and retrieve page content or selected elements for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance can run an unchecked remote installer and may introduce broader agent changes without clear user control.

Mitigation: Use a separately reviewed CLI installation, explicitly approve local changes, and review or disable automatic skill synchronization.

Risk: Cloudflare requests and credential handling are mediated by OOMOL, and the hosted connector implementation is unverified.

Mitigation: Understand the access granted to the connected Cloudflare account and review the connector's behavior before relying on it.

## Reference(s):

- [Cloudflare Browser Run documentation](https://developers.cloudflare.com/browser-run/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, HTML, JSON, Markdown, Text]

**Output Format:** [oo CLI commands with connector responses in HTML, JSON, Markdown, or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response shape depends on the selected action and its live connector schema.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
