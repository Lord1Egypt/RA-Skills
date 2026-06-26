## Description: <br>
Megan is a nutrition advisor that estimates calories, TDEE/BMR, macronutrient targets, meal plans, hydration needs, fasting options, cycle-aware nutrition guidance, and food logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yamyeed](https://clawhub.ai/user/yamyeed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to estimate nutrition targets, plan meals, track food and hydration, and receive lifestyle nutrition suggestions. The guidance is informational and is not a substitute for a qualified clinician or registered nutrition professional. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store sensitive body metrics, menstrual or reproductive-health details, allergies, food logs, and hydration data locally. <br>
Mitigation: Use it only on a trusted device, review what is stored under ~/nutrition-data, and delete that folder when the records are no longer needed. <br>
Risk: Nutrition, fasting, supplement, PCOS, pregnancy, and other medical-adjacent guidance may be inappropriate for some users. <br>
Mitigation: Treat the guidance as informational, avoid using it as a substitute for professional care, and consult a qualified clinician for medical conditions or pregnancy-related decisions. <br>
Risk: Calorie, macro, food, and restaurant estimates can be incomplete or inaccurate. <br>
Mitigation: Review estimates before relying on them and avoid unsafe restriction; the skill's own guidance includes minimum daily calorie floors and recommends professional consultation for special cases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yamyeed/nutrition-advisor) <br>
- [Publisher profile](https://clawhub.ai/user/yamyeed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown responses with nutrition estimates, tables, plans, and tracking summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local JSON records under ~/nutrition-data for profiles, daily logs, and hydration.] <br>

## Skill Version(s): <br>
4.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
