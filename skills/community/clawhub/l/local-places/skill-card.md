## Description:

Search for places (restaurants, cafes, etc.) via Google Places API proxy on localhost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steipete](https://clawhub.ai/user/steipete)

### License/Terms of Use:


## Use Case:

Agents use this skill to resolve natural-language locations and search for nearby places through a locally running Google Places API proxy, then present structured place results and optional details to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included server can expose an unauthenticated Google Places API-key proxy beyond localhost, creating billing and quota risk.

Mitigation: Run the server on loopback only, avoid binding to 0.0.0.0 unless authentication and network controls are added, and restrict the Google API key in Google Cloud.

Risk: Location searches may send sensitive home, work, or routine location details to Google and may appear in validation-error logs.

Mitigation: Avoid submitting sensitive location details unless the user accepts that exposure, and review logs for sensitive request bodies before sharing or retaining them.

Risk: Changing GOOGLE_PLACES_BASE_URL can redirect requests and API credentials to an untrusted host.

Mitigation: Keep GOOGLE_PLACES_BASE_URL unset or set only to a trusted Google Places-compatible endpoint.

## Reference(s):

- [Local Places ClawHub Skill](https://clawhub.ai/steipete/skills/local-places)
- [Google Places API v1 Endpoint](https://places.googleapis.com/v1)
- [Local Places Source Homepage](https://github.com/Hyaxia/local_places)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with curl examples and JSON request/response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local FastAPI server and GOOGLE_PLACES_API_KEY.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
