## Description:

Operate Baixiao AI through the oo CLI for literature search, citation verification, research discovery, metadata lookup, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and academic staff use this skill to search Baixiao's scholarly databases and knowledge bases, verify citations, retrieve metadata and PDFs, explore grants and policies, and invoke supported tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI setup flow executes a remote installer whose contents and exact deployed behavior have not been verified.

Mitigation: Review and install a verified CLI release before use.

Risk: The CLI may install additional agent skills during startup.

Mitigation: Decide whether synchronized skills are acceptable; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: The call_tool action can change Baixiao state, and PDF retrieval consumes account credits.

Mitigation: Keep write confirmations enabled and review the cost before retrieving a PDF.

## Reference(s):

- [oo CLI documentation](https://github.com/oomol-lab/oo-cli)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Baixiao AI homepage](https://www.know-pa.cn/)

## Skill Output:

**Output Type(s):** [API results, Structured research data, Shell commands]

**Output Format:** [JSON results and shell command instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on connected account access and live action schemas; PDF retrieval consumes credits.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
