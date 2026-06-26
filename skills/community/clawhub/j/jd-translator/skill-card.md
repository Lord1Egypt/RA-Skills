## Description: <br>
Analyzes job descriptions by translating role requirements into company problems and structured interview preparation materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and interview coaches use this skill to turn a pasted job description into a four-layer analysis, problem tree, capability-to-business-need mapping, self-introduction guidance, interview questions, and resume optimization suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted job descriptions, resumes, or company context may contain sensitive personal or business information. <br>
Mitigation: Review and redact sensitive details before sharing inputs with an agent or downstream model. <br>
Risk: The skill may answer in Chinese by default, which can be unsuitable for some users or review workflows. <br>
Mitigation: Ask explicitly for the preferred output language when invoking the skill. <br>
Risk: Interview-preparation analysis can be incomplete or misleading when the job description lacks company, team, or industry context. <br>
Mitigation: Provide the full JD and relevant company or industry background, then review the generated strategy before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/jd-translator) <br>
- [Publisher profile](https://clawhub.ai/user/lj22503) <br>
- [four-layer-framework.md](references/four-layer-framework.md) <br>
- [c-end-analysis.md](examples/c-end-analysis.md) <br>
- [b-end-analysis.md](examples/b-end-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional shell command guidance for the local JD parser] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be in Chinese unless the user asks for another language; analysis quality depends on the completeness of the provided job description and company context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
