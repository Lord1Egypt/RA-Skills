## Description:

专为OPC、个人发明者、初创企业设计，提供专利、商标、软著三类知识产权全方位保护与运营工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT

## Use Case:

External founders, individual inventors, and startup IP leads use this skill to plan patent, trademark, and software copyright work, generate first-draft materials, and organize filing checklists. It is intended as IP workflow assistance rather than a substitute for professional legal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential invention details or patent search terms may leave the user's machine when Zhiyuya API credentials are configured.

Mitigation: Use local or free-tool guidance unless intentionally using the API, and manually review what technical details are sent to third-party services.

Risk: The documented MCP server is unpinned and would receive API credentials if enabled.

Mitigation: Avoid enabling the MCP server unless the package source is verified and the version is pinned.

Risk: Generated patent, trademark, or software copyright materials may be incomplete or legally incorrect.

Mitigation: Treat outputs as drafts and have a qualified professional review filings and strategy before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-ip-toolkit)
- [Patent application workflow](references/patent-workflow.md)
- [Trademark registration workflow](references/trademark-workflow.md)
- [Software copyright workflow](references/software-copyright.md)
- [TRIZ innovation method](references/triz-innovation.md)
- [External API integration guide](references/api-integration.md)
- [Zhiyuya Open Platform](https://open.zhihuiya.com/)
- [CNIPA.AI](https://cnipa.ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional Python scripts, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use third-party patent APIs when credentials are intentionally configured; otherwise produces local guidance, checklists, and draft templates.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
