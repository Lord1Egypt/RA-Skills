## Description:

This Chinese-language skill diagnoses psychology paper Method sections across six dimensions and returns a structured scoring report with revision suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjinhongmy-pixel](https://clawhub.ai/user/wangjinhongmy-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

External academic writers, students, and reviewers use this skill to combine six Method-section diagnostics into a weighted summary report. It helps identify the weakest writing dimensions, apply mandatory downgrade rules, and prioritize revisions before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on six named diagnostic sub-skills; missing or untrusted dependencies can produce incomplete or inconsistent summaries.

Mitigation: Verify that the six dependency skills are installed, trusted, and named as expected before relying on the summary report.

Risk: Academic writing guidance may be incomplete or misleading if source diagnostics are wrong or applied outside psychology Method sections.

Mitigation: Have a qualified reviewer validate the final recommendations before applying them to a manuscript submission.

## Reference(s):

- [Method Diagnostic Summary Rubric](artifact/references/rubric.md)
- [ClawHub Skill Page](https://clawhub.ai/wangjinhongmy-pixel/skills/method-diagnostic-summary)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs weighted scores, dimension ratings, mandatory downgrade status, issue summaries, and prioritized revision guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
