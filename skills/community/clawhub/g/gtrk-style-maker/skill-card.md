## Description:

通过证据驱动的访谈，帮助视频创作者提炼自己的视觉语法，并生成可执行的栏目技能、共享词表和配置登记。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

视频栏目创作者可用它通过作品、反例和实际工序梳理个人视觉规则，并将规则整理成可执行的技能文件、共享词表及栏目配置。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 生成的技能内容可能包含不准确或误导性指导。

Mitigation: 安装前审阅并扫描生成的技能内容。

Risk: 安装的技能可能影响多个 Agent；链接的源文件后续改动也会改变其行为。

Mitigation: 审阅源文件，并只选择预期受影响的 Agent 作为安装目标。

Risk: 安装过程会执行本次审阅范围之外的外部 npm 包代码。

Mitigation: 安装前检查所用包及其来源，并在受控环境中运行安装步骤。

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gitruck/skills/gtrk-style-maker)
- [Gitruck CLI project homepage](https://github.com/Gitruck/cli)

## Skill Output:

**Output Type(s):** [Files, Markdown, Configuration instructions, Shell commands, Guidance]

**Output Format:** [可执行技能目录（Markdown 文件及按需资源）与栏目配置登记，附安装说明]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [根据访谈证据定制；技能可由用户选择安装到指定 Agent。]

## Skill Version(s):

1.3.10 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
