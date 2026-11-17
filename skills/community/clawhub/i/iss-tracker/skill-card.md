## Description:

Get the real-time location (latitude/longitude) of the International Space Station.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharkbytescs](https://clawhub.ai/user/sharkbytescs)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve and display the current latitude and longitude of the International Space Station.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a third-party ISS location service over HTTP, so location data could be tampered with on the network and the service can observe the request.

Mitigation: Review the data source before relying on the coordinates, and prefer an HTTPS location source when authenticated or privacy-sensitive location data matters.

## Reference(s):

- [ISS current location API endpoint](http://api.open-notify.org/iss-now.json)
- [ClawHub skill page](https://clawhub.ai/sharkbytescs/skills/iss-tracker)
- [Publisher profile](https://clawhub.ai/user/sharkbytescs)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text coordinates produced by a shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; retrieves data from the Open Notify ISS endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
