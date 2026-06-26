## Description: <br>
Job Screener Engine helps job seekers evaluate role opportunities with a structured scoring framework, company research prompts, and action recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calmdowntr](https://clawhub.ai/user/calmdowntr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Job seekers use this skill after receiving an interview invitation, offer, job description, or concrete role lead to score the opportunity across salary, company maturity, growth potential, work pace, stability, and location. It helps them decide whether to apply, interview, compare opportunities, or decline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask for sensitive job-search preferences and store them in a local user profile file. <br>
Mitigation: Review the profile before use, keep it local, redact details that are not needed for scoring, and delete it when it is no longer useful. <br>
Risk: The skill uses WebSearch to research companies and roles, which can disclose target company or role names to the search tool and may return incomplete information. <br>
Mitigation: Use the skill only when those searches are acceptable, require cited source snippets for searched claims, mark unverified information clearly, and ask the user for missing details before scoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calmdowntr/skills/job-screener-engine) <br>
- [Scoring framework](references/scoring_framework.md) <br>
- [Setup wizard](references/setup_wizard.md) <br>
- [Information checklist](references/info_checklist.md) <br>
- [User profile template](references/user_profile.TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports with scoring tables, concise follow-up questions, and optional local Markdown profile configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WebSearch evidence for company research and asks up to three concrete questions when key role details are missing.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
