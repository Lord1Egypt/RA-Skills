## Description:

Enables AI-powered parsing and key information extraction from high-frequency documents including invoices, orders, receipts, long texts, and common Chinese identity and credential documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

Developers, AI agent builders, and enterprise operations teams use this skill to configure and invoke Laiye ADP CLI workflows for document parsing, structured field extraction, custom extraction apps, batch processing, and asynchronous result queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-use setup may install mutable remote or unpinned global software before processing sensitive documents.

Mitigation: Review the skill before installation, use a pinned and verified CLI installation path, and avoid pipe-to-shell or immediate PowerShell execution from mutable URLs.

Risk: The workflow can upload invoices, identity documents, HR files, financial records, local files, or URL lists to Laiye ADP.

Mitigation: Only process documents the user is authorized to send to Laiye ADP, and confirm the selected regional API base URL before use.

Risk: API keys and app caches are required for operation and may be stored outside the conversation.

Mitigation: Confirm where credentials and application caches are stored, avoid exposing API keys in prompts or logs, and clear configuration when it is no longer needed.

Risk: The artifact license says commercial use requires explicit written authorization.

Mitigation: Confirm Laiye's commercial authorization terms before using the skill for revenue-generating or customer-facing work.

## Reference(s):

- [ADP CLI command reference](references/commands.md)
- [ADP CLI response schema](references/response-schema.md)
- [ADP CLI examples](references/examples.md)
- [ADP CLI error handling guide](references/error-handling.md)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- [ADP China portal](https://adp.laiye.com/)
- [ADP Global portal](https://adp-global.laiye.com/)
- [Laiye Technology](https://laiye.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing CLI workflows may create exported result files when ADP commands are run with export options.]

## Skill Version(s):

1.10.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
