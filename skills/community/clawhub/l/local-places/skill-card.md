## Description: <br>
Search for places such as restaurants and cafes through a localhost Google Places API proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Local Places to resolve natural-language locations, search nearby places with filters, and retrieve place details through a local FastAPI proxy backed by Google Places. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the API server on 0.0.0.0 can expose the local Google Places proxy beyond the intended localhost-only use. <br>
Mitigation: Run the server with the 127.0.0.1 command from SKILL.md unless network exposure is intentional and protected by additional controls. <br>
Risk: Location searches and place-detail requests are sent to Google Places and may reveal user location intent. <br>
Mitigation: Use the skill only for searches that users are comfortable sending to Google Places. <br>
Risk: A misconfigured GOOGLE_PLACES_BASE_URL could route requests and API credentials to an untrusted endpoint. <br>
Mitigation: Leave GOOGLE_PLACES_BASE_URL unset or set it only to a trusted Google Places endpoint. <br>
Risk: Validation logging can include raw request bodies that may contain location queries. <br>
Mitigation: Review or remove raw request-body logging before regular use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/steipete/local-places) <br>
- [Publisher profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown instructions with curl examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search limits and filters are constrained by the local API schema; requests require GOOGLE_PLACES_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
