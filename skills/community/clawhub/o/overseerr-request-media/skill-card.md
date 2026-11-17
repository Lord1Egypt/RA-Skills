## Description:

Request movies or TV shows on a user's Overseerr instance by searching titles, checking availability or prior requests, and submitting movie, series, or season-specific requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trialskid](https://clawhub.ai/user/trialskid)

### License/Terms of Use:


## Use Case:

Users with an Overseerr instance use this skill to ask an agent to request movies or TV shows, including specific seasons, after checking whether the media is already available or already requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented TV-season request example repeats the request endpoint and may submit the same authenticated request incorrectly or twice if followed literally.

Mitigation: Review or correct the season-specific request command before use so only one Overseerr request endpoint is sent.

Risk: The skill sends media search and request data to the user's configured Overseerr service using an API key.

Mitigation: Use a trusted Overseerr URL, protect OVERSEERR_API_KEY, and confirm users are comfortable with the media data sent to that service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trialskid/skills/overseerr-request-media)
- [ClawHub publisher profile](https://clawhub.ai/user/trialskid)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Short Markdown confirmations, clarification prompts, and request-status messages with shell command examples in the source guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's OVERSEERR_URL and OVERSEERR_API_KEY environment variables to search and submit requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
