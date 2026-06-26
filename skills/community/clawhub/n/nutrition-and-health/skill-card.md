## Description: <br>
Provides personalized meal, drink, nutrition, fitness, and general wellness guidance, with Chinese-first documentation and English trigger support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for everyday meal planning, drink choices, nutrition habits, fitness eating, stomach-friendly options, and general wellness suggestions. It can also ask profile questions to tailor recommendations to preferences, goals, and health context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask for sensitive health details such as age, weight, health conditions, allergies, habits, and goals. <br>
Mitigation: Use it only when users are comfortable sharing that context in their OpenClaw environment, and avoid entering medical details that should not appear in prompts, logs, or conversation history. <br>
Risk: The skill gives broad nutrition and wellness guidance that may be mistaken for medical advice. <br>
Mitigation: Treat recommendations as general wellness support, not diagnosis or treatment, and consult a qualified clinician for serious symptoms, chronic disease management, allergies, medication interactions, or medically restricted diets. <br>
Risk: The skill can activate on ordinary food and health questions, increasing the chance that users rely on generic guidance for a specific personal situation. <br>
Mitigation: Review suggestions against the user's actual constraints, preferences, and professional medical advice before acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhuqingsonga/nutrition-and-health) <br>
- [Skill Instructions](SKILL.md) <br>
- [README](README.md) <br>
- [Usage Tips](tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Configuration] <br>
**Output Format:** [Markdown or conversational text with lists, examples, and profile questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local JSON knowledge files and locally supplied user profile details to tailor suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
