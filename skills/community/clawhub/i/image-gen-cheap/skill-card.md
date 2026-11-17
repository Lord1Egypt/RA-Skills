## Description:

Image Gen Cheap helps agents generate and edit images through the LaoZhang API using supported text-to-image and image-editing models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enihsago](https://clawhub.ai/user/enihsago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate images from text prompts and edit images from image URLs through LaoZhang API-backed scripts. The skill is suited to agent workflows that need image URLs, saved image files, or optional JSON API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and the LaoZhang bearer token are sent to LaoZhang's API.

Mitigation: Use the skill only when that data sharing is acceptable, and review LaoZhang's policies before submitting sensitive or confidential images.

Risk: API tokens may be exposed if stored loosely or passed directly on the command line.

Mitigation: Store ~/.laozhang_api_token with restrictive permissions such as chmod 600 and avoid putting bearer tokens in shell history.

Risk: Dependency versions are not pinned in the artifact documentation.

Mitigation: Install requests in a pinned or otherwise controlled Python environment before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enihsago/skills/image-gen-cheap)
- [LaoZhang API registration](https://api.laozhang.ai/register/?aff_code=lfa0)
- [LaoZhang chat completions endpoint](https://api.laozhang.ai/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, JSON]

**Output Format:** [Markdown guidance with inline shell commands; scripts print image URLs, optional JSON API responses, and save image files locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images default to a generated-images directory; URL-returning models print URLs and base64-returning models are decoded before saving.]

## Skill Version(s):

1.0.1 (source: evidence.release.version, created 2026-04-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
