## Description: <br>
Query DeepWiki MCP service via Streamable HTTP to get GitHub repository documentation, wiki structure, and AI-powered Q&A. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhedev](https://clawhub.ai/user/liuhedev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to query DeepWiki for documentation, wiki structure, and AI-assisted Q&A about public GitHub repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository names, paths, and questions are sent to DeepWiki. <br>
Mitigation: Use this skill only for public repositories and non-sensitive questions; do not include secrets, credentials, private repository identifiers, or confidential business details. <br>
Risk: DeepWiki responses may be incomplete, outdated, or misleading for downstream decisions. <br>
Mitigation: Review returned documentation and Q&A before using it as authoritative project guidance. <br>


## Reference(s): <br>
- [LH OpenClaw Kit homepage](https://github.com/liuhedev/lh-openclaw-kit) <br>
- [DeepWiki MCP endpoint](https://mcp.deepwiki.com/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/liuhedev/lh-deepwiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Plain text or Markdown printed to stdout from DeepWiki MCP responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports ask, structure, and contents commands for public GitHub repositories.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
