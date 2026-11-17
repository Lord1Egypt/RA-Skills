## Description:

君黎AI拆书把用户提供的本地 .txt 长篇网络小说拆成可复用的创作参考包，固定产出 1 份书籍画像、6 张方法卡和若干案例卡，用于后续写作参考与案例检索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljunn](https://clawhub.ai/user/ljunn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writing-focused agents use this skill to turn a local Chinese web-novel text file into reusable writing-reference assets. It is intended for book profiling, method extraction, and searchable case cards rather than plot summaries, literary criticism, character dossiers, continuations, or new-book planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads a user-selected local novel text file and generated chunk files may retain excerpts or full portions of that source text.

Mitigation: Use a dedicated ./story workspace, avoid private or unrelated .txt files, and review local generated files before sharing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljunn/skills/junli-story-analysis)
- [Practical workflow](artifact/references/practical-workflow.md)
- [Analysis pipeline](artifact/references/analysis-pipeline.md)
- [Chunk card guide](artifact/references/chunk-card-guide.md)
- [Mode selection](artifact/references/mode-selection.md)
- [Quality checklist](artifact/references/quality-checklist.md)
- [Output templates](artifact/references/output-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and local project folders produced through a command-line workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a dedicated story workspace with chunks, extraction cards, drafts, a book profile, six method cards, and as many case cards as the source supports.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
