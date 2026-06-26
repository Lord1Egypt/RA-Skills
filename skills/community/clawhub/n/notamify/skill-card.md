## Description: <br>
Retrieve and analyze NOTAMs (Notices to Airmen) for airports worldwide using the Notamify Python SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[damians21](https://clawhub.ai/user/damians21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External aviation users, pilots, dispatchers, and developers use this skill to query active, nearby, historical, and briefing NOTAM data for flight planning and situational awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a NOTAMIFY_TOKEN and queries an external aviation-data API. <br>
Mitigation: Run it only in an environment you control, provide the token through environment or config mechanisms, and do not hardcode credentials in generated scripts. <br>
Risk: NOTAM summaries or recommendations may be incomplete, stale, or unsuitable as the sole basis for operational flight decisions. <br>
Mitigation: Use the output for informational flight planning support and verify operational decisions against official NOTAM sources. <br>
Risk: The skill may install and execute a third-party Python SDK. <br>
Mitigation: Review the package and run generated Python scripts in a controlled Python environment before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/damians21/notamify) <br>
- [Notamify API documentation](https://skymerse.gitbook.io/notamify-api) <br>
- [Notamify Python SDK documentation](https://skymerse.gitbook.io/notamify-api/sdk/python) <br>
- [Notamify API manager](https://notamify.com/api-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks plus concise NOTAM summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install and use the third-party notamify-sdk package, requires NOTAMIFY_TOKEN, and should remind users to verify operational decisions against official NOTAM sources.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
