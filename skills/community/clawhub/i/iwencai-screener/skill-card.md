## Description:

根据输入的链接、文件、文本或关键词分析利好行业/概念/题材/产业链，聚焦核心受益方向，在i问财网站进行选股查询，返回每项前5个结果并生成Excel文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[caobingxi](https://clawhub.ai/user/caobingxi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze links, files, text, or keywords for Chinese-market stock-screening intent, identify 3-5 core beneficial sectors or concepts, query i问财, and return structured stock results with an Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-activate broadly, fetch or read user-supplied content, and write Excel files.

Mitigation: Ask for confirmation before reading local files or writing Excel output, and restrict exports to a controlled directory.

Risk: Generated spreadsheets and stock selections may be treated as verified financial advice.

Mitigation: Treat outputs as unverified analysis and validate stock data and conclusions against trusted financial sources before use.

Risk: Weak spreadsheet-safety controls may allow unsafe or misleading workbook content to reach users.

Mitigation: Review generated workbook contents before opening, sharing, or importing them into other systems.

## Reference(s):

- [i问财](https://www.iwencai.com)
- [ClawHub skill page](https://clawhub.ai/caobingxi/skills/iwencai-screener)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown stock-screening analysis plus generated Excel workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to five stock results per selected direction and writes a multi-sheet Excel file when export succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
