## Description:

上传岗位描述（JD）和个人简历后，该技能会生成面试题预测、STAR 答题框架、简历与 JD 匹配度分析以及 Markdown 备考手册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career coaches use this skill to turn a job description and resume into targeted interview preparation material, including likely questions, STAR response guidance, gap analysis, and a reusable preparation handout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Résumé and job-description content may be sent to the configured LLM provider.

Mitigation: Use only content you are comfortable sharing with that provider, obtain appropriate consent, and redact contact details or other unnecessary personal data before use.

Risk: A misconfigured API base could route sensitive interview-preparation content to an untrusted service.

Mitigation: Verify that OPENAI_API_BASE points to a trusted HTTPS endpoint before running the skill.

Risk: Optional document parsing dependencies expand the local execution environment.

Mitigation: Install parsing dependencies in a dedicated virtual environment and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonia-sz/skills/jd-interview-prep)
- [ClawHub publisher profile](https://clawhub.ai/user/antonia-sz)
- [Default LLM API endpoint](https://api.deepseek.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with match analysis, predicted interview questions, STAR answer guidance, and preparation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print the report to standard output or save it to a user-provided Markdown file path.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
