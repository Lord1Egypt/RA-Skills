## Description:

LinkFoxAI lets an agent call the LinkFox AI open platform for image and video generation workflows, including model swaps, cutouts, image expansion, scene variation, product image sets, talking sales videos, image-to-video, task polling, generic API calls, and connectivity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this skill to connect an agent to LinkFox AI media-generation APIs, submit authenticated image or video jobs, poll for results, and return generated media URLs or API responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authenticated access to LinkFox AI APIs and media upload workflows.

Mitigation: Use a scoped API key if available, protect LINKFOXAI_API_KEY, and review proposed api-call and upload-base64 commands before execution.

Risk: Media, prompts, product data, and account credentials are sent to LinkFoxAI/Ziniao services.

Mitigation: Install only when that data sharing is acceptable, and avoid uploading sensitive local files or private/person media without consent.

Risk: Changing LINKFOXAI_BASE_URL can route authenticated requests away from the documented official hosts.

Mitigation: Keep LINKFOXAI_BASE_URL on the documented official hosts unless the deployment has separately verified the endpoint and allowlist requirements.

Risk: Generated media jobs can take a long time, fail audit checks, or return temporary result URLs.

Mitigation: Run long jobs in background sessions, poll status, surface task IDs and error messages, and refresh expired result URLs when needed.

## Reference(s):

- [LinkFox AI Open Platform](https://open.ziniao.com)
- [LinkFox API Guide](https://www.linkfox.com/team/api-guide)
- [AI Image and Video API Reference](references/image-make.md)
- [Open Platform Access and Error Codes](references/open-platform.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses or generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include temporary generated media URLs, task IDs for polling, API error messages, and configuration requirements for LinkFoxAI credentials.]

## Skill Version(s):

1.5.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
