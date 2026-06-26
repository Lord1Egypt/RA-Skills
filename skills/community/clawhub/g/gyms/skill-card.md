## Description: <br>
Find nearby gyms when the user asks for fitness centers near them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to find gyms near a user-provided or authorized location, with optional radius, result limit, and amenity filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use a user's current or approximate location to search for gyms. <br>
Mitigation: Request location permission before use and prefer approximate or grid-obfuscated coordinates when exact location is unnecessary. <br>
Risk: The referenced standard response document is not packaged with the skill. <br>
Mitigation: Treat the missing document as unavailable unless separately provided, and return a clear point-of-interest list using the fields available from the request and search results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mikeclaw007/gyms) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Structured data] <br>
**Output Format:** [Markdown or structured point-of-interest list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-authorized location; default radius is 3000 meters, default limit is 20, and maximum limit is 50.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
