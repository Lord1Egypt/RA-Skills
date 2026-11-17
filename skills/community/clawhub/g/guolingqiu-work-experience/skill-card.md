## Description:

A Chinese-language career coaching skill that uses Guolingqiu's three-year work history across platform operations, e-commerce product management, project management, and AI product management to help job seekers structure experience, write resumes, and prepare for interviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurezyx](https://clawhub.ai/user/futurezyx)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-speaking job seekers use this skill for resume drafting, interview preparation, work-experience analysis, and career-positioning guidance based on structured career records and industry reference material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes that the advice is narrowly framed around young women job seekers.

Mitigation: Review the demographic framing before deployment and adapt the guidance style when serving broader or more neutral career-coaching audiences.

Risk: The security guidance flags broad activation wording for this career coaching skill.

Mitigation: Review trigger terms and deployment scope so the skill is installed only where Chinese-language, persona-styled career coaching is desired.

Risk: The artifact supports supplementing work-experience details with industry-common knowledge, which could be mistaken for a user's real work history.

Mitigation: Require users to verify and edit generated resume or interview content against their actual experience before using it professionally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/futurezyx/skills/guolingqiu-work-experience)
- [Career data reference](references/career-data.md)
- [Industry knowledge reference](references/industry-knowledge.md)
- [Interview guide reference](references/interview-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown responses with structured coaching guidance, resume bullets, interview prompts, and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language, persona-styled career coaching output; no code execution or persistence indicated by security evidence]

## Skill Version(s):

1.0.0 (source: frontmatter, clawhub.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
