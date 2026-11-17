## Description:

电机设计一体化工作流 | 串联极槽配合→磁路计算→Maxwell仿真→FOC参数配置全流程，输出完整设计报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongjie666888](https://clawhub.ai/user/yongjie666888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and motor-design engineers use this Chinese-language skill to structure a motor design workflow from requirements through pole-slot selection, magnetic-circuit estimates, Maxwell simulation planning, winding design, and FOC parameter configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Engineering formulas, example values, and generated FOC code may be inaccurate or incomplete for a specific motor or controller.

Mitigation: Use the skill as a design aid only and validate calculations, simulation results, and controller parameters with qualified engineering review before applying them to real hardware.

Risk: FOC configuration guidance could lead to unsafe behavior if transferred directly to a physical motor system.

Mitigation: Test generated parameters in simulation or a controlled bench setup with conservative current, voltage, and thermal limits before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yongjie666888/skills/motor-design-integration)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown design report with code and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow guidance; engineering values and generated controller settings require professional validation before hardware use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
