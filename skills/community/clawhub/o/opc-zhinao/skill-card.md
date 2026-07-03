## Description: <br>
OPC智脑为一人创业者提供五阶段创业诊断、可行度评分、MVP设计、合规落地、冷启动增长、报告导出和反馈收集支持。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sober568](https://clawhub.ai/user/sober568) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and solo founders use this skill to diagnose their startup stage, score business feasibility, choose the next operating step, and generate actionable markdown or HTML reports. Agent builders can also use its prompts and TypeScript examples to integrate the five-stage workflow into supported IDEs and AI platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer scripts can overwrite existing project agent instruction files such as AGENTS.md or IDE-specific instruction files. <br>
Mitigation: Inspect the target project first, keep backups of existing instruction files, and install only into a backed-up or disposable project directory. <br>
Risk: Installer cleanup prompts can delete the source directory if accepted. <br>
Mitigation: Decline cleanup unless the source path is disposable and never run installers with elevated privileges unless independently reviewed. <br>
Risk: The feedback workflow records and summarizes user feedback locally, which can retain sensitive business details. <br>
Mitigation: Avoid entering confidential business information unless local retention is acceptable, and review or delete opc-feedback/ records after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sober568/opc-zhinao) <br>
- [Publisher profile](https://clawhub.ai/user/sober568) <br>
- [OPC智脑 official website](http://opc.soberli.com) <br>
- [Source repository listed by release artifact](https://gitee.com/zx_allen_li/opc_skills.git) <br>
- [README.md](README.md) <br>
- [五阶段创业诊断模型](docs/stage-model.md) <br>
- [Skill参考手册](docs/skill-reference.md) <br>
- [集成指南](docs/integration-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional JSON configuration, TypeScript examples, shell commands, and Markdown or HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local diagnosis reports under opc-reports/ and feedback records under opc-feedback/ when the user chooses export or feedback flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
