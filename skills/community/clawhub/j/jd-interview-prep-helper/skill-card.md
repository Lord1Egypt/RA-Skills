## Description:

Help users prepare for job interviews by analyzing job descriptions and company information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ting2tao](https://clawhub.ai/user/ting2tao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and job candidates use this skill to turn a job description, company name, and optional role context into a structured interview preparation guide with technical focus areas, company research, practice topics, behavioral prompts, and a study plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the skill to run for general interview-prep requests where the user has not provided enough context.

Mitigation: Ask for the job description, company, target role, and any missing constraints before producing a full preparation plan.

Risk: Interview preparation may involve resumes, job descriptions, or other personal files.

Mitigation: Use only files the user intentionally provides for the preparation task and avoid requesting sensitive personal data unless it is necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ting2tao/skills/jd-interview-prep-helper)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance, files]

**Output Format:** [Markdown interview preparation guide]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save the preparation guide as an interview-prep markdown file when the agent has write access.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
