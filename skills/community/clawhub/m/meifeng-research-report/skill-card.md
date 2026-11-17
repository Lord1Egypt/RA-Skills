## Description:

为国网公司人力资源管理咨询项目撰写研究或调研报告，基于用户提供的政策文件、研究文献和调研数据生成结构化 Word 文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[meifeng1998](https://clawhub.ai/user/meifeng1998)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, consultants, and analysts working on State Grid or similar state-owned enterprise HR-management projects use this skill to turn authorized source materials into formal research reports on reform, performance assessment, compensation, governance, and incentive mechanisms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided policy files, HR materials, or research inputs may contain confidential or sensitive information.

Mitigation: Use only documents the user is authorized to process and review the generated report before sharing it.

Risk: Generated report language could include inaccurate claims if source materials are incomplete or ambiguous.

Mitigation: Require policy provisions, data points, and citations to come from user-provided inputs, and mark unverifiable content as pending verification.

Risk: The skill writes a Word document and could overwrite an existing report file.

Mitigation: Ask the agent to use a new filename or confirm before replacing an existing .docx file.

## Reference(s):

- [国网人力资源管理研究分析框架参考](references/分析框架参考.md)
- [国网研究报告文档风格规范](references/文档风格规范.md)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [Word document (.docx) with structured report prose, citations to user-provided materials, and optional tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should use authorized input materials, mark unverifiable claims as pending verification, and avoid overwriting existing .docx files without confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
