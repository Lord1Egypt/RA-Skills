## Description: <br>
Personal Health Tool Free helps individual users record health data, interpret common checkup indicators, generate exercise plans, provide diet guidance, and summarize health trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External individual users use this skill with an agent to manage personal health records, checkup summaries, exercise plans, diet guidance, goals, reminders, and trend summaries. Its health guidance is informational and not a substitute for professional medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive health data through the hosting agent or model provider despite local-storage claims. <br>
Mitigation: Use only health data acceptable for the configured agent/model provider or run with local processing; restrict file access to the intended ~/.health directory where possible. <br>
Risk: Health summaries and checkup interpretations may be mistaken for medical diagnosis or care instructions. <br>
Mitigation: Treat outputs as informational guidance and consult a qualified clinician for abnormal indicators, symptoms, medication decisions, or treatment plans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/personal-health-tool-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON examples, Python snippets, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read local health data under ~/.health when the hosting agent grants file-system access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
