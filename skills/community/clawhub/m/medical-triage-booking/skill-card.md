## Description: <br>
Provides consumer-facing medical triage support by collecting symptoms and history, checking emergency warning signs, suggesting likely departments, ranking matching Beijing hospital and doctor options, generating booking reminders, and preparing map-route links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunlinlin-aragon](https://clawhub.ai/user/sunlinlin-aragon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to get triage-oriented department suggestions, Beijing hospital and doctor recommendations, registration guidance, appointment reminder times, and route-planning links. It is intended as triage assistance and navigation support, not diagnosis or medical treatment. <br>

### Deployment Geography for Use: <br>
China (Beijing-focused) <br>

## Known Risks and Mitigations: <br>
Risk: Route planning can infer or share sensitive location data without clear consent or provider disclosure. <br>
Mitigation: Ask the user to confirm route planning before using location data, prefer approximate manually entered starting points, and disclose that Baidu Maps receives route-planning data. <br>
Risk: Medical triage and hospital recommendations may be mistaken for diagnosis or treatment advice. <br>
Mitigation: Present outputs as triage assistance only, preserve emergency escalation guidance, and advise users to consult qualified medical professionals for diagnosis or treatment. <br>
Risk: Hospital data may include incomplete, non-clinical, or stale entries. <br>
Mitigation: Flag uncertain matches, review Top 3 recommendations before presenting them, and direct users to hospital registration desks or official booking channels when data quality is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunlinlin-aragon/medical-triage-booking) <br>
- [Publisher profile](https://clawhub.ai/user/sunlinlin-aragon) <br>
- [Medical triage rules](references/triage_rules.md) <br>
- [Baidu geocoding API endpoint](https://api.map.baidu.com/geocoding/v3/) <br>
- [Baidu directions link endpoint](http://api.map.baidu.com/direction?) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, api calls, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON outputs from helper scripts and route links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top 3 hospital, department, and doctor matches; emergency flag; reminder times; optional Baidu map route link.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
