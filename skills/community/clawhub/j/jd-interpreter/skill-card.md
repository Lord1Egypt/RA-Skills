## Description: <br>
招聘需求智能解读技能，可将粘贴、上传或 URL 来源的岗位 JD 转换为 8 维结构化解读，并生成交互式 HTML 可视化报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers and career advisors use this skill to understand job descriptions before tailoring resumes or preparing for interviews. It extracts role facts, explicit and implicit requirements, weighted priorities, self-assessment prompts, interview topics, learning paths, ATS keywords, and optional salary context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted job-description content can be rendered into a local interactive HTML report without escaping or sanitizing all fields. <br>
Mitigation: Use only trusted JD inputs, review generated HTML before opening or sharing it, and update the report generator to escape fields and disable inline script execution where feasible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bettermen/jd-interpreter) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/bettermen) <br>
- [analysis.json Schema Reference](references/analysis_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured analysis, analysis.json, and an interactive HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates jd-interpretation-report.html from analysis.json; optional salary benchmarking may use web search when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
