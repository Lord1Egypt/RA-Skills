## Description:

go-now is a Chinese-language travel planning companion that helps users clarify travel intent, compare destinations and booking options, and generate a personalized visual itinerary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bradleo](https://clawhub.ai/user/bradleo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use go-now when they have vague travel intent, choice fatigue, or trip-planning hesitation and want conversational help turning that intent into concrete destinations, booking options, next steps, and a shareable visual itinerary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use IP-based location services to infer the user's city.

Mitigation: Ask for consent before calling external location endpoints, offer manual city entry, and disclose which service will receive the request.

Risk: The skill may include personal details such as names, avatar URLs, vehicle plates, or companions in a generated itinerary.

Mitigation: Collect personal details only after opt-in, include only details the user provided, and omit sensitive identifiers unless they are necessary.

Risk: The skill may save and open a personalized HTML itinerary on the user's machine.

Mitigation: Confirm before writing or opening the file, show the target path, and allow the user to review the generated content first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bradleo/skills/go-now)
- [Demo itinerary template](artifact/references/demo-template.html)
- [ipinfo.io location endpoint](https://ipinfo.io/json)
- [ip-api location endpoint](https://ip-api.com/json/)
- [myip.ipip.net location endpoint](https://myip.ipip.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown conversation responses with inline shell commands and self-contained HTML itinerary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save and open a personalized HTML itinerary on the user's desktop.]

## Skill Version(s):

1.0.0 (source: release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
