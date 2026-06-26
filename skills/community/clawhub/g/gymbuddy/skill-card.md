## Description: <br>
GymBuddy helps agents provide Chinese-language fitness guidance for posture correction, body-composition and training-data analysis, periodized training plans, and TDEE estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyxin-del](https://clawhub.ai/user/joeyxin-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to answer fitness questions, discuss posture and training plans, estimate daily energy expenditure, and route pain, injury, pregnancy, chronic disease, neurological, or cardiovascular concerns to qualified professionals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fitness, posture, and nutrition advice may be mistaken for medical diagnosis or treatment. <br>
Mitigation: Treat outputs as informational and refer pain, injury, pregnancy, chronic disease, neurological symptoms, or cardiovascular concerns to a qualified clinician or in-person professional. <br>
Risk: The skill can run bundled local Python helpers to estimate TDEE and create a knowledge index. <br>
Mitigation: Review the commands before execution and keep use limited to the included local calculator and index builder unless the operator approves broader changes. <br>


## Reference(s): <br>
- [GymBuddy ClawHub release page](https://clawhub.ai/joeyxin-del/gymbuddy) <br>
- [Cursor Agent Skills documentation](https://docs.cursor.com) <br>
- [Claude Code Skills documentation](https://docs.anthropic.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with optional inline shell commands and numeric TDEE estimates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primarily Chinese-language coaching output; fitness, posture, and nutrition guidance is informational and should not be treated as medical diagnosis or treatment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
