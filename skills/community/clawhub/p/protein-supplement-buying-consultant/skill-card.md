## Description: <br>
Guides users buying protein powder or supplements through goal, dietary, and health questions to determine the exact type, form, protein content, and purity specification they need. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbazex](https://clawhub.ai/user/arbazex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to choose a protein supplement for a purchase decision based on goals, diet, allergies, health context, activity level, anti-doping needs, form preferences, and region. The agent gathers the required context, calculates a daily protein target and supplement gap, produces prioritized specification lists, and only then suggests matching products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks about health context and protein intake, which could be mistaken for medical nutrition guidance. <br>
Mitigation: Treat outputs as general buying advice, not medical advice, and direct users with kidney or liver disease, pregnancy, breastfeeding, children, teenagers, or medically restricted diets to a clinician or registered dietitian. <br>
Risk: The skill may suggest purchasable supplement products after the consultation. <br>
Mitigation: Require the agent to finish the consultation and specification lists first, present product suggestions as starting points for user research, and avoid endorsements or automated purchases. <br>
Risk: The consultation can involve sensitive health, diet, allergy, and body weight details. <br>
Mitigation: Ask only for details needed to determine supplement specifications and avoid collecting unrelated personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arbazex/protein-supplement-buying-consultant) <br>
- [Skill homepage](https://github.com/arbazex/fitness-equipment-buying-consultants/tree/master/protein-supplement-buying-consultant) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Conversational text and structured Markdown with calculations, prioritized specification lists, safety flags, and numbered product suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Product suggestions are capped at five and must follow the consultation and specification lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
