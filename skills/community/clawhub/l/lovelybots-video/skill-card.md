## Description:

Generate TikTok-style talking videos from a script and image using the LovelyBots API, then poll for completion and return the video URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgegally](https://clawhub.ai/user/georgegally)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, ecommerce brands, developers, and agent pipelines use this skill to create talking video assets from a script and image through the LovelyBots API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts, images, prompts, and related metadata are sent to LovelyBots for external video generation.

Mitigation: Use only content appropriate for external processing and avoid submitting confidential or sensitive material unless the user has approved that use.

Risk: The LovelyBots API key is required for use and could authorize video generation if exposed.

Mitigation: Store the key as a secret environment variable, avoid committing it to source control, and rotate or revoke it if exposure is suspected.

Risk: Share URLs may grant access to generated media.

Mitigation: Prefer private video settings when appropriate and treat share URLs as access-bearing links.

Risk: Polling too aggressively or without a timeout can increase API load and delay useful user feedback.

Mitigation: Use bounded polling with retry guards, respect rate-limit responses, and report queued or processing status with the job ID and share URL.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/georgegally/skills/lovelybots-video)
- [LovelyBots OpenClaw Documentation](https://lovelybots.com/openclaw)
- [LovelyBots Developer API Key](https://lovelybots.com/developer)
- [LovelyBots API Base URL](https://api.lovelybots.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include queued job status, credits remaining, share URLs, and completed video URLs when returned by the LovelyBots API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
