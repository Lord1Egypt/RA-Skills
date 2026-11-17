## Description:

Diagnoses vocabulary and academic language issues in psychology paper Method sections, checking academic verbs, fixed expressions, terminology, and formal register with scores and journal examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjinhongmy-pixel](https://clawhub.ai/user/wangjinhongmy-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Academic writers, editors, and research assistants use this skill to review English psychology Method sections for vocabulary, collocation, terminology, and formal-register issues before manuscript revision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is strict and opinionated, so its diagnostic feedback may overstate issues for manuscripts outside English psychology Method sections.

Mitigation: Use it for the intended manuscript section and treat findings as review guidance that an author or editor confirms before revision.

Risk: The bundled artifact and skill text disagree on the positive-example directory path, which may affect example retrieval after packaging.

Mitigation: Verify the packaged references directory during release validation and confirm that example lookup resolves before deployment.

Risk: Academic-writing diagnostics can influence manuscript quality and interpretation.

Mitigation: Require human review of suggested changes and retain the original manuscript as the source of truth.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjinhongmy-pixel/skills/method-vocabulary-diagnostic)
- [Method vocabulary checklist](references/checklist.md)
- [Method vocabulary scoring rubric](references/rubric.md)
- [Positive example reference set](references/examples/)
- [Detected DOI reference: 10.1037/pspp0000572](https://doi.org/10.1037/pspp0000572)
- [Detected DOI reference: 10.1037/dev0002073](https://dx.doi.org/10.1037/dev0002073)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic report with score tables, issue lists, revision suggestions, and reference examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagnosis only; it does not rewrite the manuscript.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
