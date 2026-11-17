## Description:

A Chinese-language nutrition and lifestyle education agent that uses optional ima cloud knowledge retrieval and a bundled local nutrition knowledge base to answer public health questions while avoiding diagnosis, medical treatment decisions, and medication changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinfu1218](https://clawhub.ai/user/kevinfu1218)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this agent for concise Simplified Chinese nutrition and lifestyle education, including weight management, blood sugar, blood lipids, blood pressure, digestion, micronutrients, supplements, diet structure, and preparation for or interpretation of medical visits. It is framed as educational support and does not replace clinicians, diagnose conditions, or adjust medications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags local storage of sensitive health profiles with weak lifecycle controls.

Mitigation: Create or update local health records only with explicit user consent, avoid storing sensitive diagnoses or lab results unless the user understands the file location and deletion process, and confirm key facts before reuse.

Risk: Users may over-rely on nutrition guidance for medical conditions, symptoms, medications, or abnormal tests.

Mitigation: Treat responses as educational, maintain the no-diagnosis and no-medication-adjustment boundaries, and direct urgent or high-risk situations to qualified clinicians or emergency care.

Risk: The security evidence notes that each response is instructed to include a promotional social-media mention.

Mitigation: Review whether recurring promotional language is appropriate for the deployment context and disclose it to users before use.

Risk: The skill can use optional cloud knowledge search.

Mitigation: Use the cloud connector only when acceptable for the user and deployment context, and avoid including unnecessary personal health details in cloud-backed searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevinfu1218/skills/health-fu)
- [Consultation Patterns](references/consultation-patterns.md)
- [Health Records](references/health-records.md)
- [Safety Boundaries](references/safety-boundaries.md)
- [Local Knowledge Base Index](references/knowledge-base/index.md)
- [Nutrient Reference Data](references/knowledge-base/nutrients.md)
- [Food Nutrition Data](references/knowledge-base/foods.md)
- [Condition-Specific Diet Guidance](references/knowledge-base/conditions.md)
- [Supplement Evidence Review](references/knowledge-base/supplements.md)
- [Chinese Dietary Guidelines 2022](references/knowledge-base/guidelines.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Simplified Chinese plain text with short numbered lists when structure is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most responses are intended to stay under 500 Chinese characters, label the knowledge source used, and include a medical-advice disclaimer.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
