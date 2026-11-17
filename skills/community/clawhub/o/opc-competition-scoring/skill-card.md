## Description:

A Chinese-language agent skill for business competition judges that applies a five-dimension, 100-point scoring rubric to business plans and produces reports, rankings, comments, and review prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Competition judges, mentors, and event operators use this skill to standardize first-round or semifinal reviews of startup and business-plan submissions. It helps produce scoring reports, ranking tables, issue lists, and follow-up questions for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles participant business plans and proposes broad background checks, which can involve sensitive personal, company, or competition data.

Mitigation: Use it only with explicit authority to process the materials, disclose any external verification sources, minimize retained data, and avoid non-public social-security or tax records.

Risk: Automated scoring can influence judging outcomes even when the analysis is incomplete or mistaken.

Mitigation: Require qualified human judges to review scores, deductions, rankings, and comments before they are used in competition decisions.

Risk: The included batch script discovers submitted files but currently scores placeholder content instead of parsing the actual documents.

Mitigation: Do not rely on the script as-is for real judging; validate document extraction separately or use manually reviewed extracted text as input.

Risk: The online verification module can create privacy, consent, and source-quality issues if applied without boundaries.

Mitigation: Run external checks only with separate consent and source-by-source disclosure, and treat results as review prompts rather than final determinations.

## Reference(s):

- [打分标准参考表](references/打分标准表.md)
- [常见扣分点清单](references/常见扣分点.md)
- [优秀案例库](references/优秀案例库.md)
- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-competition-scoring)
- [Publisher profile](https://clawhub.ai/user/golngod)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, ranking tables, JSON summaries, structured review comments, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes individual scoring reports, batch ranking outputs, deception-risk flags, missing-information checks, and judge review prompts.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
