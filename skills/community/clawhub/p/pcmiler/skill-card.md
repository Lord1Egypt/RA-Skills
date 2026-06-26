## Description: <br>
PC*Miler REST API helper guidance for retrieving route geometry, route reports, and geocoded coordinates for trucking workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nchoudhury-trimble](https://clawhub.ai/user/nchoudhury-trimble) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to call PC*Miler REST endpoints for truck route paths and address geocoding with an authenticated API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent needs access to a PC*Miler API key. <br>
Mitigation: Use a dedicated key where possible, store it as a secret environment variable, and avoid exposing it in prompts, logs, or shared outputs. <br>
Risk: Route stops, coordinates, and addresses are sent to PC*Miler when the API examples are used. <br>
Mitigation: Avoid submitting sensitive personal or operational locations unless PC*Miler handling terms are acceptable for the intended use. <br>


## Reference(s): <br>
- [ClawHub PC*Miler skill page](https://clawhub.ai/nchoudhury-trimble/pcmiler) <br>
- [PC*Miler routeReports API example](https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/route/routeReports?stops=-75.173297%2C39.942892%3B-74.83153%2C39.61703%3B-74.438942%2C39.362469&reports=RoutePath) <br>
- [PC*Miler locations API example](https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/locations?street=1%20Independence%20Way&city=princeton&state=nj&country=US&postcode=08540&postcodeFilter=us&region=NA&dataset=Current) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and a valid PCMILER_API_KEY; API calls send route stops, coordinates, or addresses to PC*Miler.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
