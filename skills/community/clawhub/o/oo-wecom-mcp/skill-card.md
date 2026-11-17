## Description:

Operate WeCom MCP through an OOMOL-connected account to inspect available tools and perform approved WeCom actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WeCom users use the skill to inspect the connected WeCom tools and run requested actions through OOMOL. Actions that change or remove data require explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions can trigger unverified remote code execution through an installer fallback.

Mitigation: Install and verify a specific CLI release yourself, and prevent automatic execution of its installer fallback. Review the CLI's agent-skill installation behavior and the permissions granted through OOMOL.

Risk: The WeCom connector may expose actions that send, overwrite, cancel, or delete data.

Mitigation: Keep explicit approval for WeCom changes, and confirm the exact payload and effect before running state-changing or destructive actions.

## Reference(s):

- [WeCom MCP homepage](https://work.weixin.qq.com)
- [WeCom API documentation](https://open.work.weixin.qq.com/help2/pc/21676)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell examples, JSON action payloads, and connector results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action fields depend on the live WeCom connector schema; state-changing and destructive actions require approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
