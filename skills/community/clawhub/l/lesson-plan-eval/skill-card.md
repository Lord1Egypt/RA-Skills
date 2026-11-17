## Description:

Evaluates Chinese vocational education lesson plans using Bloom's taxonomy, Gagne learning outcomes, Marzano's taxonomy, the 5E model, and vocational teaching standards to identify concrete design problems and improvement paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, teaching researchers, and vocational education reviewers use this skill to audit lesson plans for measurable objectives, instructional-method fit, authentic activities, question progression, learner analysis, and alignment between goals, content, and assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may generate incorrect or overly harsh educational critique or scoring if the submitted lesson plan is incomplete or ambiguous.

Mitigation: Review the diagnostic tables and scores before using them in teaching decisions, and provide missing objectives, key points, difficulties, and process details when prompted.

Risk: Optional Word export can create a local .docx file and may require installing Pandoc.

Mitigation: Review any package-install command before running it and use Markdown-only output when local document generation is not needed.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/flyboat403/lesson-plan-eval)
- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/lesson-plan-eval)
- [Publisher profile](https://clawhub.ai/user/flyboat403)
- [Output template](artifact/references/output-template.md)
- [Pandoc conversion guide](artifact/references/pandoc-guide.md)
- [Scoring standard](artifact/references/scoring-standard.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown reports with diagnostic tables, scoring summaries, improvement guidance, and optional Pandoc command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language lesson-plan audit output; may ask the user to choose Markdown, Word export, or summary-only delivery after evaluation.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; source skill frontmatter declares 0.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
