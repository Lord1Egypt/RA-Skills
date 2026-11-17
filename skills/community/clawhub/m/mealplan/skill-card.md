## Description:

Mealplan is a command-line meal organizer that logs meal entries locally and exposes commands for listing meals, planning days, nutrition, shopping lists, and random meal suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Mealplan to organize weekly meal records through shell commands, including adding meals, listing meals for a day, and requesting simple planning, nutrition, shopping, or random suggestion output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell argument handling can expose arbitrary local files readable by the user account.

Mitigation: Review and fix argument handling and quoting before deployment; until then, run the skill only with trusted meal, date, and type inputs.

Risk: Planning, nutrition, shopping, and random suggestion commands may overstate what the script actually provides.

Mitigation: Treat those outputs as simple helper text and verify meal plans, nutrition information, and shopping lists before relying on them.

Risk: Meal data is stored locally under ~/.local/share/mealplan/.

Mitigation: Avoid entering sensitive diet or health details unless local storage is acceptable, and manage or delete the stored JSON Lines file according to user or organization policy.

## Reference(s):

- [Mealplan on ClawHub](https://clawhub.ai/bytesagain1/skills/mealplan)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text command output with JSON Lines local meal records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The add command writes meal records under ~/.local/share/mealplan/.]

## Skill Version(s):

3.0.0 (source: frontmatter, script, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
