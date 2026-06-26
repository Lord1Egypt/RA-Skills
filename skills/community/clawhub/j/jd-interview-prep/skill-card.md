## Description: <br>
上传岗位描述和个人简历后，AI 会预测常见、针对性和追问类面试题，提供 STAR 答题框架，分析简历与 JD 的匹配度，并导出备考手册。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job candidates, career coaches, and agents preparing for interviews use this skill to compare a resume against a job description, identify gaps, and generate a Markdown interview-prep handbook with likely questions and STAR guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume and job-description content can be sent to the configured LLM provider, which defaults to DeepSeek unless changed. <br>
Mitigation: Redact contact details and confidential employer information first, then confirm the API key, endpoint, and provider are approved for the user's data. <br>
Risk: Exported interview-prep reports can contain sensitive career, employer, and personal details. <br>
Mitigation: Write exported Markdown reports only to private locations and review them before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antonia-sz/jd-interview-prep) <br>
- [Default DeepSeek API endpoint](https://api.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with match analysis, interview questions, STAR guidance, and optional exported .md file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a timestamped interview preparation handbook when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
