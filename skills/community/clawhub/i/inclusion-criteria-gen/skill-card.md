## Description:

Generate and optimize clinical trial subject inclusion/exclusion criteria to balance scientific rigor with recruitment feasibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical operations, medical writing, and protocol design teams use this skill to draft, optimize, analyze, and benchmark clinical trial eligibility criteria while considering recruitment feasibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loose file access and installation guidance could lead to unintended local file reads or writes.

Mitigation: Run the CLI only with trusted input and output paths inside a dedicated workspace, and install it in an isolated environment.

Risk: Unpinned or unnecessary dependency installation could increase supply-chain review burden.

Mitigation: Avoid running pip install -r requirements.txt unless dependencies are removed or pinned and reviewed.

Risk: Clinical trial criteria drafts may contain sensitive protocol information or patient-level data.

Mitigation: Do not provide PHI, secrets, or confidential protocol material unless approved local storage and review controls are in place.

Risk: Generated eligibility changes may be mistaken for clinical or regulatory decisions.

Mitigation: Treat generated criteria, optimization notes, and benchmark outputs as drafting aids that require qualified clinical, regulatory, and operational review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/inclusion-criteria-gen)
- [Optimization Guidelines for Inclusion/Exclusion Criteria](references/optimization_guidelines.md)
- [Common Pitfalls in Eligibility Criteria Design](references/common_pitfalls.md)
- [Regulatory Guidance on Eligibility Criteria](references/regulatory_guidance.md)
- [Criteria Templates](references/criteria_templates.json)
- [Feasibility Data](references/feasibility_data.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and CLI/Python usage patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce JSON criteria files, optimization reports, complexity analyses, and benchmark placeholder reports when the bundled CLI is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
