## Description: <br>
Plan meals with calorie tracking and shopping lists. Use when organizing weekly meals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Mealplan to organize weekly meals, track calories, review nutrition summaries, generate shopping lists, and request meal suggestions from local meal history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal and calorie history is stored locally under ~/.local/share/mealplan. <br>
Mitigation: Avoid entering sensitive health details unless local storage is acceptable, and remove ~/.local/share/mealplan to clear saved data. <br>
Risk: Using the skill runs a local Bash script. <br>
Mitigation: Review the script and run it in an environment where local file writes to the mealplan data directory are acceptable. <br>


## Reference(s): <br>
- [Mealplan on ClawHub](https://clawhub.ai/bytesagain1/mealplan) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can append local JSON Lines meal entries under ~/.local/share/mealplan when the add command is used.] <br>

## Skill Version(s): <br>
3.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
