## Description:

对照用户提供的两版专利文本，保留新增、删除和替换原文及行号，并输出差异表和离线对照页；不推断法律范围或修改支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

专利从业者或研究人员可用它对照同一材料的旧稿和新稿，定位逐行文字变化并追溯两侧原文。默认在本地处理用户已有文本；只有用户要求补取数据时才使用可选在线客户端。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional online client may produce unsafe spreadsheet exports.

Mitigation: Treat imported candidate CSV columns as text before opening or processing them.

Risk: The optional client’s trial-key cache may be insufficiently protected, especially on shared computers or Windows.

Mitigation: Keep the credential cache private; use the offline comparison path for confidential drafts. Before retrieval, approve the search terms and budget.

## Reference(s):

- [Local workflow and comparison limits](references/local-workflow.md)
- [Comparison pitfalls](references/pitfalls.md)
- [Optional API reference](references/api-reference.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [CSV change table, standalone offline HTML comparison, JSON statistics, and a concise source-linked summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Line-based text comparison that preserves source wording; reports textual differences without legal conclusions. The HTML view works offline.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
