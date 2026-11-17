## Description:

Transform and restyle existing videos using AI via Media.io OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to call Media.io OpenAPI endpoints for credit checks, task result retrieval, and video-to-video transformation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests may send the user's Media.io API key to unintended Media.io API paths when path parameters are not validated and URL-encoded.

Mitigation: Review task IDs and path parameters before invocation, avoid values supplied by untrusted content, and prefer a release that validates and URL-encodes path parameters before sending authenticated requests.

## Reference(s):

- [Media.io Platform Documentation](https://platform.media.io/docs/)
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/skills/mediaio-video-to-video-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API responses with concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io API key supplied through API_KEY or an explicit api_key argument.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
