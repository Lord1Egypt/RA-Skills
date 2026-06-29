## Description: <br>
AI-powered insurance agent training coach that parses product documents, generates question banks, assesses agent skill levels, schedules personalized daily training, and supports interactive role-play sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Insurance trainers, agency leaders, and insurance technology teams use this skill to create coaching materials, question banks, competency assessments, daily training plans, and role-play practice for insurance agents. Outputs are advisory training materials that require qualified human review before use in sales, compliance, or product recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports included Python scripts with external lottery API calls despite the skill text claiming there are no scripts or network calls. <br>
Mitigation: Review the scripts before installation, disable or remove lottery-data functions unless explicitly needed, and restrict outbound network access in regulated or enterprise deployments. <br>
Risk: The skill can create insurance sales, compliance, and product recommendation training content that may be incorrect, outdated, or unsuitable for a specific jurisdiction or product. <br>
Mitigation: Require review by licensed insurance and compliance professionals before using generated materials with agents or customers. <br>
Risk: Training scenarios may involve agent, client, schedule, or product information that could include personal or sensitive data. <br>
Mitigation: Do not provide real customer PII, use synthetic or redacted examples, and align any data handling with applicable privacy and insurance compliance requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gechengling/skills/insurance-agent-trainer) <br>
- [Question bank templates](references/question_bank_templates.md) <br>
- [Agent profile template](references/agent_profile_template.md) <br>
- [Training evaluation rubric](references/training_evaluation_rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Analysis, Guidance, Configuration] <br>
**Output Format:** [Markdown and JSON-style structured training artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product profiles, question banks, competency assessments, daily training plans, role-play scripts, scoring rubrics, and human-review reminders.] <br>

## Skill Version(s): <br>
5.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
