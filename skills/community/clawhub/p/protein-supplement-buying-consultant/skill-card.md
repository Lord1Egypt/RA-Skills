## Description:

Guide users buying protein powder or supplements through goal, dietary, and health questions to determine the exact type, form, protein content, and purity spec they need -- allergy-aware, brand-neutral.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping-assistant agents use this skill to evaluate protein supplement options based on goals, allergies, dietary restrictions, health context, activity level, anti-doping needs, and country. It produces a structured specification recommendation before suggesting matching products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence supplement purchases and discusses health-related constraints.

Mitigation: Users with medical conditions, pregnancy or breastfeeding concerns, or questions for children should follow the skill guidance to consult a qualified healthcare professional before relying on recommendations.

Risk: Recommendations can be misleading if the user has not provided the required goal, allergy, health, body-weight, activity, anti-doping, and region context.

Mitigation: The skill requires critical intake questions before recommendation generation and asks targeted follow-up questions when answers are vague or incomplete.

Risk: Product suggestions may become unsuitable as labels, certifications, ingredients, or regional availability change.

Mitigation: The skill frames product suggestions as starting points for the user's own research and emphasizes verification of third-party certifications, labels, and certificates of analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbazex/skills/protein-supplement-buying-consultant)
- [Project homepage](https://github.com/arbazex/fitness-equipment-buying-consultants/tree/master/protein-supplement-buying-consultant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown consultation with structured recommendations, safety flags when triggered, and product suggestions after required intake questions are answered]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external APIs, environment variables, runtime dependencies, or hidden system access are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
