## Description:

Sif (sif.com). Use this skill for ANY Sif request — searching and reading data. Whenever a task involves Sif, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon marketplace researchers and sellers can use this skill through a connected Sif account to explore product, keyword, demand, and competition data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's setup instructions use a live remote CLI installer, and its local changes are not fully explained in the supplied evidence.

Mitigation: Review and approve the CLI installation separately, using a verified release where available; control automatic agent-skill synchronization before running it.

Risk: Sif requests pass through OOMOL and may consume service credits.

Mitigation: Review the applicable Sif point costs and OOMOL service-credit terms before running actions.

## Reference(s):

- [Sif homepage](https://www.sif.com)
- [Sif MCP documentation](https://blog.sif.com/article/mcp-install/Sif-MCP%E5%AE%89%E8%A3%85%E6%96%87%E6%A1%A3)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands]

**Output Format:** [JSON results and text or Markdown summaries, with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Sif account and live action schemas; some actions consume Sif points.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
