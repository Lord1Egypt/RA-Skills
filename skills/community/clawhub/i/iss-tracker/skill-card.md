## Description: <br>
Get the real-time location (latitude/longitude) of the International Space Station. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharkbytescs](https://clawhub.ai/user/sharkbytescs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, educators, and automation users can use this skill to ask an agent for the ISS's current latitude and longitude from a public API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a public HTTP API and depends on the availability and behavior of that service. <br>
Mitigation: Review the API call before execution and confirm network access to the Open Notify endpoint is acceptable for the deployment environment. <br>
Risk: The command relies on local curl and jq binaries. <br>
Mitigation: Install curl and jq only from trusted system package sources and keep them patched. <br>


## Reference(s): <br>
- [Open Notify ISS Current Location API](http://api.open-notify.org/iss-now.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/sharkbytescs/iss-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text latitude and longitude, with Markdown containing an inline bash command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires trusted system installations of curl and jq; no credentials or local files are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
