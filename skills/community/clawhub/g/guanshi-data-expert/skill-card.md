## Description: <br>
观势专家集群的数据分析专家，用于数据清洗、统计推断、财务建模、可视化和情景模拟，将原始数据转化为可支撑决策的量化洞察。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data analysts, strategists, and agent workflows use this skill to clean structured or semi-structured datasets, run statistical tests, build financial models, visualize results, and produce decision-ready analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install Python packages into the current environment when required data-analysis libraries are missing. <br>
Mitigation: Run it in an isolated environment and approve dependency installation before use. <br>
Risk: The skill reads local datasets and writes analysis outputs, which can expose sensitive data to the active agent session. <br>
Mitigation: Limit file access to the datasets needed for the task and use sanitized data where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuobadaidai/guanshi-data-expert) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown reports with tables, statistical annotations, chart file references, and optional Python-generated PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce intermediate temp files and final analysis artifacts such as charts or Markdown reports in the workspace output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
