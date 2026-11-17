## Description:

Simulates NIH study section peer review for grant proposals, generating structured critiques, NIH-style 1-9 scores, weakness analysis, revision recommendations, and mock Summary Statements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External grant writers, researchers, and research administrators use this skill to run local mock reviews of NIH-style grant drafts before submission and identify concrete revision priorities. It can review full proposals, selected sections, focused NIH criteria, score-only outputs, and before/after revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grant proposals and generated reviews may contain sensitive proposal-derived content.

Mitigation: Install and run the skill in an isolated local environment, save outputs only to intentional workspace paths, and treat generated review files as sensitive.

Risk: The artifact advertises PDF and DOCX inputs, but extraction is not implemented in the local script.

Mitigation: Use TXT or MD inputs for accurate review unless a separate, reviewed extraction step is added.

Risk: Generated scores and critiques are simulated and may not match an actual NIH study section review.

Mitigation: Use the output as preparatory feedback and supplement it with qualified human review before submission decisions.

## Reference(s):

- [NIH Scoring Rubric Reference](artifact/references/nih_scoring_rubric.md)
- [Review Criteria Explained](artifact/references/review_criteria_explained.md)
- [Common Weaknesses Catalog](artifact/references/common_weaknesses_catalog.md)
- [Summary Statement Templates](artifact/references/summary_statement_templates.md)
- [Score Calibration Guide](artifact/references/score_calibration_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/grant-mock-reviewer)
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [analysis, markdown, JSON, guidance]

**Output Format:** [Markdown Summary Statement and revision recommendations, or JSON scores when scores-only mode is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file input with optional local file output; supports full review, focused criteria, score-only output, and proposal comparison mode.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
