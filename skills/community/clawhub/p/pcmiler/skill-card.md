## Description:

PC*Miler REST API guidance helps agents retrieve route geometry and geocode addresses through authenticated PC*Miler API requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nchoudhury-trimble](https://clawhub.ai/user/nchoudhury-trimble)

### License/Terms of Use:


## Use Case:

Developers and logistics engineers use this skill to call PC*Miler for truck routing route-path reports and address-to-coordinate geocoding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API requests send addresses, coordinates, route stops, and authentication credentials to PC*Miler.

Mitigation: Use an appropriately scoped API key, keep secrets out of shared logs and scripts, and submit sensitive location data only when approved.

Risk: The skill depends on external network access and the availability of the PC*Miler API.

Mitigation: Confirm network access and API-key validity before using generated commands in an agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nchoudhury-trimble/skills/pcmiler)
- [PC*Miler route reports endpoint example](https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/route/routeReports?stops=-75.173297%2C39.942892%3B-74.83153%2C39.61703%3B-74.438942%2C39.362469&reports=RoutePath)
- [PC*Miler locations geocoding endpoint example](https://pcmiler.alk.com/apis/rest/v1.0/Service.svc/locations?street=1%20Independence%20Way&city=princeton&state=nj&country=US&postcode=08540&postcodeFilter=us&region=NA&dataset=Current)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a valid PCMILER_API_KEY environment variable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
