## Description:

Generate and edit AI images and videos with Media.io OpenAPI, including text-to-image, image-to-image, text-to-video, image-to-video, task status, and credit queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Media.io image and video generation APIs, poll asynchronous generation tasks, query credit balance, and retrieve generated output URLs from JSON responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation prompts and media URLs are sent to Media.io under the user's Media.io API key.

Mitigation: Use the skill only when Media.io's terms fit the content being sent, and avoid sensitive or private media unless those terms are acceptable.

Risk: The required Media.io API key may expose account access or consume paid generation credits if reused broadly.

Mitigation: Use a dedicated least-privilege or test key, keep credentials out of shared logs and prompts, and rotate keys if exposure is suspected.

Risk: Runtime dependencies and outbound API calls expand the execution environment's trust boundary.

Mitigation: Install dependencies in an isolated environment with pinned versions and review outbound requests before deployment.

## Reference(s):

- [MediaIO AIGC API Capability Reference](references/mediaio-aigc-api-reference.md)
- [Media.io API Documentation](https://platform.media.io/docs/)
- [Media.io Developer Portal](https://developer.media.io/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API responses with task IDs, status objects, credit balances, errors, and generated media result URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io API key and returns raw response payloads from Media.io endpoints.]

## Skill Version(s):

1.0.14 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
