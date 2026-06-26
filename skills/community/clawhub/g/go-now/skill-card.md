## Description: <br>
Go Now is a travel companion skill that helps users clarify vague travel intent, compare destination options, and move from planning to booking action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bradleo](https://clawhub.ai/user/bradleo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for conversational travel planning when they feel undecided, tired, or unsure where to go. The skill gathers preferences, recommends destinations, flights, hotels, and points of interest through FlyAI, and can generate a personalized travel-plan poster as a local HTML file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may look up the user's IP-based location through third-party services. <br>
Mitigation: Ask the user for a departure city manually unless they explicitly agree to IP-based location lookup. <br>
Risk: The skill may include personal details such as avatar URLs, companion details, or vehicle information in generated travel posters. <br>
Mitigation: Confirm which personal details should appear before generating or sharing the poster. <br>
Risk: The skill may create a local HTML file and open it in a browser. <br>
Mitigation: Confirm the save path and browser-opening behavior before creating local output. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/bradleo/go-now) <br>
- [Travel poster demo template](references/demo-template.html) <br>
- [IPInfo location endpoint](https://ipinfo.io/json) <br>
- [IP-API location endpoint](https://ip-api.com/json/) <br>
- [IPIP location endpoint](https://myip.ipip.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, HTML, files, guidance] <br>
**Output Format:** [Conversational text and Markdown recommendations, plus self-contained HTML travel-poster files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local HTML file on the user's Desktop and open it in a browser after itinerary generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
