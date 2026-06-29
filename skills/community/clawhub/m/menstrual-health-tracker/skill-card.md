## Description: <br>
Menstrual Health Tracker helps agents guide users through privacy-aware menstrual and reproductive health logging, cycle and symptom analysis, predictions, visual dashboards, and informational health suggestions across life stages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[web-seeker](https://clawhub.ai/user/web-seeker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and their agents use this skill to record menstrual and reproductive health information, analyze cycle and symptom patterns, generate local reports or dashboards, and receive informational wellness guidance. It is designed for personal tracking across menstruation, fertility planning, pregnancy, postpartum, perimenopause, and postmenopause contexts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive menstrual and reproductive health information that may be stored in local JSON files or generated HTML dashboards. <br>
Mitigation: Use it only when local storage is acceptable, keep generated files out of shared folders, and avoid sending dashboards or data files to others unless intentionally sharing private health information. <br>
Risk: Health guidance from the skill is informational and may not address a user's clinical situation. <br>
Mitigation: Treat outputs as personal tracking support, not diagnosis or treatment, and seek professional medical care for abnormal symptoms or urgent concerns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/web-seeker/menstrual-health-tracker) <br>
- [Analysis engine reference](references-en/analysis_engine.md) <br>
- [Medical standards reference](references-en/medical_standards.md) <br>
- [Life stages reference](references-en/life_stages.md) <br>
- [User profile reference](references-en/user_profile.md) <br>
- [Empathy guide reference](references-en/empathy_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text with optional JSON records, shell commands, Python analysis output, and HTML dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read a local menstrual_health.json file and generate local HTML dashboards when the user requests analysis or visualization.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
