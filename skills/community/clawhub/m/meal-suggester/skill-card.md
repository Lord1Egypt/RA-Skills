## Description: <br>
Quick dinner companion blending taste profiles, inventory tracking, and learning-based recipe rotation. Use to generate <=25-minute meals, log ingredients, and build shopping suggestions that respect both your and your partner's preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thibautrey](https://clawhub.ai/user/thibautrey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill as a household meal-planning assistant to generate quick dinner suggestions, track pantry inventory, remember taste profiles and allergies, and build shopping suggestions from meal feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores pantry contents, preferences, allergies, meal history, and shopping suggestions in local markdown notes. <br>
Mitigation: Review the local notes before installation and ask the agent to preview and confirm inventory or preference changes before writing them. <br>
Risk: The skill describes a daily 19:00 cron reminder that can create recurring meal suggestions. <br>
Mitigation: Review, adjust, or disable the cron schedule unless daily suggestions are desired. <br>
Risk: The suggestion script appends selected meals to the local history file. <br>
Mitigation: Keep the history file user-reviewable and confirm that appended meal records are appropriate for the household context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thibautrey/meal-suggester) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown recipe suggestion with local markdown inventory, history, preference, and shopping-list notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append meal suggestions to local history and relies on user-maintained pantry, allergy, preference, and feedback files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
