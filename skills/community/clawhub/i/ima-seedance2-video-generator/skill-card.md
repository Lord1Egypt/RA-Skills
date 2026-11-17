## Description:

Generates Seedance 2.0 videos from text prompts, images, first-last-frame pairs, and image, video, or audio reference media through the IMA API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenfancy-gan](https://clawhub.ai/user/allenfancy-gan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate cinematic, storyboard-driven, product, advertising, and short-form videos from prompts and reference media. The skill supports task setup, media validation, upload, polling, and result delivery for Seedance 2.0 and Seedance 2.0 Fast workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and private media can be exposed through third-party requests, uploads, logging, or unsafe URL fetching.

Mitigation: Use a scoped or test IMA key, avoid private or regulated media, and assume prompts and media URLs may appear in output or logs.

Risk: User-supplied remote media URLs can be fetched for probing and validation.

Mitigation: Avoid untrusted remote URLs and require media from trusted, directly downloadable sources.

Risk: IMA_AUTO_CONSENT can bypass interactive asset compliance confirmation.

Mitigation: Enable it only when the deployment has already disclosed and accepted third-party upload and verification behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allenfancy-gan/skills/ima-seedance2-video-generator)
- [IMA homepage](https://www.imaclaw.ai)
- [Execution Protocol](references/protocols/execution.md)
- [Event Stream Protocol](references/protocols/event-stream.md)
- [Text To Video Flow](references/flows/text-to-video.md)
- [Reference Image To Video Flow](references/flows/reference-image-to-video.md)
- [Reference Media Rules](references/limits/reference-media-rules.md)
- [Create Task Contract](references/contracts/create-task.md)
- [Payload Rules](references/contracts/payload-rules.md)
- [Credit Rules](references/contracts/credit-rules.md)
- [Security Disclosure](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON-line events and final result metadata with generated video URLs or errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMA_API_KEY; may use local preference and log files under ~/.openclaw.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
