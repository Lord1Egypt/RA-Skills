## Description:

AI interview simulation and coaching that uses a user's resume and job description to generate tailored interview questions, conduct question-by-question practice, and provide scoring with model answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangmanqi2104201431-ship-it](https://clawhub.ai/user/yangmanqi2104201431-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Candidates and interview coaches use this skill to prepare for interviews by turning resumes, job descriptions, target roles, and recent interview-experience material into a structured mock interview workflow. It supports quick model answers for single interview questions and a fuller practice flow with question sets, follow-up prompts, feedback, scoring, and a recap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process sensitive resume and job-description material through configured tools and search-derived context.

Mitigation: Share only the excerpts needed for interview preparation and remove unnecessary personal details before use.

Risk: DOCX handling may involve shell-based conversion.

Mitigation: Use trusted document sources, prefer plain text or PDF excerpts when possible, and review conversions before relying on extracted content.

## Reference(s):

- [Question generation reference](artifact/references/generate-prompt.md)
- [ClawHub skill page](https://clawhub.ai/yangmanqi2104201431-ship-it/skills/interview-prepare)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown interview questions, feedback, model answers, scoring summaries, and recap guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May incorporate user-provided resume, job description, image, URL, and search-derived context when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
