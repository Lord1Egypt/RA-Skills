## Description: <br>
Iris Pro reads a Gmail inbox, scores messages by urgency and sender importance, drafts replies for actionable emails, generates weekly inbox analytics, and produces a priority action plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams use this skill to triage Gmail messages, identify urgent or important senders, draft replies, and create local inbox reports for follow-up planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Gmail content and credentials. <br>
Mitigation: Use a dedicated Gmail app password, keep access limited to a private working environment, and review the skill before installing or running it. <br>
Risk: Email-derived Markdown and JSON reports are saved locally. <br>
Mitigation: Run the skill only in a private directory and delete generated iris_pro_report files when finished. <br>
Risk: The current privacy statement may not fully describe the privacy implications of processing inbox data. <br>
Mitigation: Treat all generated outputs as sensitive and do not rely on the privacy statement as a complete disclosure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/iris-pro) <br>
- [Iris Pro license key purchase](https://ko-fi.com/s/f75940a0ce) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Markdown, JSON, Analysis, Guidance] <br>
**Output Format:** [Markdown guidance with bash and Python code blocks; generated inbox reports are Markdown and JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scans up to 200 Gmail messages, prints console tables and draft replies, and writes dated local report files.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
