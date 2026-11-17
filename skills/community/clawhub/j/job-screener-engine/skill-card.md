## Description:

Evaluates interview and job-offer opportunities across six A-H dimensions and a global 1-5 score, producing action recommendations, interview-practice value, and risk notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calmdowntr](https://clawhub.ai/user/calmdowntr)

### License/Terms of Use:

MIT

## Use Case:

Job seekers and career-focused users use this skill after receiving an interview invitation or offer to evaluate role fit, compensation, company stability, growth potential, work culture, and location fit. It helps compare one or more opportunities without making the final career decision for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store career preferences, salary thresholds, city, employment status, and optional personal details in a local user_profile.md file.

Mitigation: Keep user_profile.md out of source control, omit fields the user does not want stored, and review the file before sharing the skill directory.

Risk: The recommended npx installation flow can introduce supply-chain risk if the resolved package or skill source is not trusted.

Mitigation: Use a pinned or otherwise trusted installer command and review the resolved skill files before enabling the skill.

Risk: The skill relies on web search and job-market signals that may be incomplete, outdated, or misleading.

Mitigation: Require source snippets for key claims, mark uncertain dimensions as unknown, and ask the user for missing critical information instead of guessing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calmdowntr/skills/job-screener-engine)
- [README](README.md)
- [Scoring framework](references/scoring_framework.md)
- [Setup wizard](references/setup_wizard.md)
- [Information checklist](references/info_checklist.md)
- [User profile template](references/user_profile.TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown evaluation report with tables, scores, citations, questions, and action recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask up to three setup or missing-information questions and may create or update a local user_profile.md when the user chooses to personalize evaluations.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter and changelog list 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
