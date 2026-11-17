## Description:

Enables agents to use Laiye ADP CLI workflows for document parsing, structured extraction, custom extraction apps, batch processing, and asynchronous result queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeane-li](https://clawhub.ai/user/jeane-li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI agent builders, and operations teams use this skill to configure and invoke Laiye ADP for parsing documents, extracting fields from invoices, orders, receipts, identity documents, and custom business files, and checking asynchronous or batch job results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions may run mutable remote installer scripts or unpinned global packages on the host.

Mitigation: Prefer a pinned, verified package; inspect installer scripts before running them; and avoid elevated privileges during installation.

Risk: Document parsing and extraction may send financial, HR, identity, or confidential documents to Laiye's ADP service.

Mitigation: Use the service only for documents the user is authorized to upload, and confirm data-handling requirements before processing sensitive files.

Risk: API keys can be exposed through shell commands, logs, or agent transcripts.

Mitigation: Treat API keys as secrets, use configuration or environment storage where practical, and avoid placing real keys directly in commands or shared logs.

## Reference(s):

- [Skill Instructions](SKILL.md)
- [README](README.md)
- [Command Reference](references/commands.md)
- [Response Schema Reference](references/response-schema.md)
- [Error Handling Guide](references/error-handling.md)
- [Usage Examples](references/examples.md)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- [Laiye Technology](https://laiye.com/en/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to produce or export structured JSON results from Laiye ADP commands.]

## Skill Version(s):

1.10.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
