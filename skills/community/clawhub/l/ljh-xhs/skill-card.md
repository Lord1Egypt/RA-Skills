## Description:

ljh-xhs helps users evaluate and decompose Xiaohongshu image-text commerce posts by grading sample quality, reconstructing the user path, breaking down cover and content variables, and producing controlled variant plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and commerce content teams use this skill to analyze Xiaohongshu image-text posts, decide whether a sample is reliable enough to decompose, and turn the analysis into testable content variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-run onboarding displays promotional LJHskill content and writes an onboarding marker under the user's home directory.

Mitigation: Review the first-run message before deployment and run the skill only where creating a home-directory onboarding marker is acceptable.

Risk: Archive behavior may read or update local ljh-档案 brand files and save analysis deliverables in the current workspace.

Mitigation: Use an isolated workspace for sensitive campaigns or explicitly opt out of archive behavior when local records should not be kept.

Risk: Weak or non-comparable Xiaohongshu samples can lead to misleading viral-performance conclusions.

Mitigation: Apply the skill's A/B/C/D sample grading and treat initial factor analysis as hypotheses until controlled variants provide supporting data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-xhs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown analysis template with structured checklists and optional local archive files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask follow-up questions, grade samples from A to D, and save brand-analysis records when archive behavior is accepted.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
