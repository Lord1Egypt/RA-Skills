## Description: <br>
AI-driven health checkup report interpreter that turns report images, indicator values, or natural language descriptions into interactive HTML visualization reports with indicator interpretation, risk assessment, and personalized health recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users provide health checkup report images, structured lab values, or plain-language descriptions to receive a readable report that highlights abnormal indicators, trends, risk levels, and follow-up suggestions. The skill is for health education and report understanding, not diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive health information from reports and user descriptions. <br>
Mitigation: Redact names, ID numbers, phone numbers, hospital IDs, and other identifiers before use; keep generated reports private. <br>
Risk: Generated interpretations or recommendations may be incomplete or inaccurate for an individual medical situation. <br>
Mitigation: Use the output for health education only and rely on a qualified clinician for diagnosis, treatment, urgent symptoms, or abnormal findings. <br>
Risk: Generated HTML reports can preserve private health details if saved or shared. <br>
Mitigation: Store reports securely, avoid sharing them publicly, and remove personal details before sending them to others. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/health-report-reader) <br>
- [Indicator reference library](references/indicators.md) <br>
- [HTML report template](references/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown containing a complete static HTML report, health indicator interpretation, risk labels, charts, and follow-up guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Chart.js-based visualization, responsive layout, print styling, and a medical disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
