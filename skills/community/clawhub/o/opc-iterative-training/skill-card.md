## Description: <br>
Skill迭代训练工具，通过双轨对照法（Freestyle vs Skill执行）持续优化Skill质量 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golngod](https://clawhub.ai/user/golngod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and skill maintainers use this skill to train and improve other skills through paired freestyle and skill-guided runs, comparison analysis, iteration logs, and regression checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad, semi-automatic revisions to other skills, including SKILL.md and reference documents. <br>
Mitigation: Restrict each run to a named target skill and review diffs before accepting any skill or reference-document change. <br>
Risk: The workflow may request access to project-management files such as skill call records or weekly reports. <br>
Mitigation: Require approval before reading project-management files and limit access to the files needed for the current training task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/golngod/opc-iterative-training) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance, comparison notes, iteration logs, and proposed skill-file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to SKILL.md or reference documents; changes should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
