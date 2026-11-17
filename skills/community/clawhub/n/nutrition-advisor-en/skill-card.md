## Description:

For users explicitly requesting nutrition help, provide English-language calorie and macro estimates, meal planning, food substitutions, restaurant estimates, and requested food or hydration logs without diagnosing or treating medical conditions, managing pregnancy or eating disorders, or accessing health data by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamyeed](https://clawhub.ai/user/yamyeed)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request practical nutrition estimates, everyday meal planning, food comparisons, and explicitly requested food or hydration tracking for generally healthy adults. The skill keeps estimates adjustable and directs medical or higher-risk situations to a licensed clinician or registered dietitian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted food and hydration records are plaintext and may be accessible to local programs or backups.

Mitigation: Keep data in the conversation by default; before persistent tracking, disclose the fields, exact path, purpose, and plaintext risk, then wait for explicit confirmation.

## Reference(s):

- [ClawHub Release](https://clawhub.ai/yamyeed/skills/nutrition-advisor-en)
- [Calculations and Estimation](references/calculations-and-estimation.md)
- [Logging and Local Storage](references/logging-and-storage.md)
- [Special Contexts and High-Risk Boundaries](references/special-contexts.md)
- [NIH Office of Dietary Supplements](https://ods.od.nih.gov/factsheets/list-all/)
- [NCCIH Herbs at a Glance](https://www.nccih.nih.gov/health/herbsataglance)
- [Academy of Nutrition and Dietetics](https://www.eatright.org/)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, JSON]

**Output Format:** [Conversational text; JSON for explicitly requested saved logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Nutrition values are estimates; persistent logs are created only after explicit user confirmation.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
