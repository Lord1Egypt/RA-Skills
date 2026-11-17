## Description:

老孟中文编程（ZHC）语言内核与智能体协作技能。当需要编写、编译、运行、诊断 ZHC 源码（.zc 文件），或需要把表格数据导出为 CSV/XLSX/DOCX/HTML，或需要查询中文关键字、内置函数、中文错误码与契约版本时使用本技能。适用于纯中文编程教学、中文代码生成、中文报错诊断与 Office 文档产出场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxh678988](https://clawhub.ai/user/mxh678988)

### License/Terms of Use:

MIT-0

## Use Case:

开发者和使用中文编程的智能体可用它编写、编译、运行和诊断 ZHC（.zc）程序，并查询语言关键字、内置函数、错误码及契约。需要时也可将表格数据导出为 CSV、XLSX、DOCX 或 HTML。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the release suspicious: its summary reports that inspection mode may run WebAssembly, build steps have temporary-file risks, and some content was not fully inspected. The partial scan does not establish that the skill is safe.

Mitigation: Before installing, review the inspection and build behavior, clarify which tools the skill may use, and seek complete analysis of the partially inspected runner and image.

## Reference(s):

- [ZHC language and Office export contract](references/契约_1.8_全量参考.md)
- [ZHC quick reference](references/快速参考.md)
- [ZHC error code reference](references/错误码表_E_1.5.md)
- [ClawHub skill release](https://clawhub.ai/mxh678988/skills/laomeng-zhc)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance, Files]

**Output Format:** [Chinese text and Markdown, .zc source code, shell commands, and CSV/XLSX/DOCX/HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the requested programming, diagnosis, or document-export task.]

## Skill Version(s):

1.0.15 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
