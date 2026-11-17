## Description:

Provides Chinese-language consumer medical triage, department selection, Top 3 Beijing hospital and doctor matches, 114/Jingtong booking guidance, appointment reminders, and Baidu Maps route links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunlinlin-aragon](https://clawhub.ai/user/sunlinlin-aragon)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this Chinese-language skill to turn symptoms and appointment details into safety triage, suggested departments, Beijing hospital and doctor matches, booking reminders, and route planning support. It is a decision-support aid and not a medical diagnosis.

### Deployment Geography for Use:

China, with Beijing-specific hospital, booking, and route-planning workflows.

## Known Risks and Mitigations:

Risk: Route planning may expose sensitive origin, destination, and hospital-intent data to Baidu Maps or an unspecified IP-geolocation provider.

Mitigation: Ask for user consent before location lookup, prefer user-entered origins, and document the external map-service data flow.

Risk: Generated Baidu map direction links use an insecure HTTP URL.

Mitigation: Change generated map links to HTTPS before production use.

Risk: The route-planning helper includes a hard-coded Baidu Maps key fallback.

Mitigation: Remove the fallback key, require BAIDU_MAP_AK from the environment, and rotate any exposed key.

Risk: Medical triage and matching output could be mistaken for diagnosis or definitive care advice.

Mitigation: Keep the output framed as triage support, preserve emergency escalation guidance, and require clinical review for deployment.

## Reference(s):

- [Medical triage and recommendation reference](references/triage_rules.md)
- [ClawHub skill page](https://clawhub.ai/sunlinlin-aragon/skills/medical-triage-booking)
- [Baidu Maps geocoding endpoint](https://api.map.baidu.com/geocoding/v3/)
- [Baidu Maps direction link endpoint](http://api.map.baidu.com/direction?)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON helper-script outputs and map links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include emergency triage flags, department candidates, Top 3 hospital/department/doctor matches, reminder times, and route links.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
