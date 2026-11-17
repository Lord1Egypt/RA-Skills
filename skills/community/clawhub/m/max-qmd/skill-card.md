## Description:

Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonnenberglauramarie-afk](https://clawhub.ai/user/sonnenberglauramarie-afk)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to index local files and run BM25, vector, hybrid, and document lookup searches through qmd.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a mutable GitHub-hosted Node package.

Mitigation: Install only from a trusted or reviewed qmd source, and pin or review the exact revision when possible.

Risk: The qmd index can retain searchable copies or representations of local private content.

Mitigation: Index only directories intended for agent-assisted search and review the qmd cache scope before enabling the skill.

## Reference(s):

- [qmd GitHub package](https://github.com/tobi/qmd)
- [Project homepage](https://tobi.lutke.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may reference local file paths, qmd collections, the Ollama endpoint, and the qmd cache location.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
