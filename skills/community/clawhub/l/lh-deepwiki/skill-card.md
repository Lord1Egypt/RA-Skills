## Description:

Query DeepWiki MCP service via Streamable HTTP to get GitHub repository documentation, wiki structure, and AI-powered Q&A.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhedev](https://clawhub.ai/user/liuhedev)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to query DeepWiki for public GitHub repository documentation, wiki structure, specific wiki content, and documentation-grounded Q&A.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository names, wiki paths, and user questions are sent to DeepWiki's external MCP service.

Mitigation: Use the skill only with public GitHub repositories and avoid sending sensitive prompts or private repository details.

Risk: The skill documentation is primarily in Chinese, which may make usage notes harder to review for non-Chinese-speaking users.

Mitigation: Translate and review the usage notes before deployment when the reviewer does not read Chinese.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuhedev/skills/lh-deepwiki)
- [Source repository homepage](https://github.com/liuhedev/lh-openclaw-kit)
- [DeepWiki MCP endpoint](https://mcp.deepwiki.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Command-line text output from DeepWiki, suitable for use in Markdown or agent responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports ask, structure, and contents commands for public GitHub repositories.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
