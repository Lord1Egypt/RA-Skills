## Description: <br>
Connects an agent to Juying Cloud Platform devices so users can list devices, read status, refresh state, and open or close relay channels using their own API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liupster](https://clawhub.ai/user/liupster) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate devices connected to the Juying Cloud Platform, including listing devices, checking state, refreshing readings, and controlling specific relay channels after device and channel identity are clear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Juying Cloud API token that can authorize access to a user's connected devices. <br>
Mitigation: Use a limited or revocable token when available, never hardcode or share tokens, and prompt for a token only when needed. <br>
Risk: The skill can open or close real device channels, which may affect physical equipment. <br>
Mitigation: Confirm the exact device and channel before control commands, avoid guessing when the request is ambiguous, and add an extra confirmation step for safety-critical equipment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liupster/juyingiot) <br>
- [Juying Cloud OpenAPI base URL](https://openapi.iot02.com/api/v1) <br>
- [Overview](artifact/overview.md) <br>
- [Endpoints](artifact/endpoints.md) <br>
- [Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP endpoints, headers, and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires each user to provide their own Juying Cloud API_Token in the Authorization header.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
