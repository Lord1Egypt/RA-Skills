## Description:

用统一脚本执行 pdf2zh-next，支持单个或多个 PDF、目录批处理、glob 筛选、可选 provider 参数、实时监控与并行翻译。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxingchtongaelofficial2568](https://clawhub.ai/user/mxingchtongaelofficial2568)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to run pdf2zh-next from an agent workflow for translating PDF files or batches of PDFs into Chinese while selecting a configured translation provider when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected PDF contents may be sent to the configured translation provider.

Mitigation: Review config.toml before use and choose a local or trusted provider for sensitive documents.

Risk: An untrusted executable path could run unexpected code through the wrapper.

Mitigation: Use the installed pdf2zh-next CLI from a trusted environment and avoid passing an untrusted --exe-path.

## Reference(s):

- [pdf2zh-next advanced documentation](https://pdf2zh-next.com/zh/advanced/advanced.html)
- [ClawHub skill page](https://clawhub.ai/mxingchtongaelofficial2568/skills/pdf2zh-translator)
- [ClawHub publisher profile](https://clawhub.ai/user/mxingchtongaelofficial2568)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and references to generated PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local pdf2zh-next CLI wrapper and writes translated PDF outputs to the selected output directory.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
