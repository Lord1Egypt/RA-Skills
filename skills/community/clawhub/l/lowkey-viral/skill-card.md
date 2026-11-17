## Description:

Create short-form social media videos and photo carousel slideshows using the lowkey viral API for TikTok, Instagram Reels, carousel posts, and other vertical social formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiotdev](https://clawhub.ai/user/tiotdev)

### License/Terms of Use:


## Use Case:

Developers, creators, and social media teams use this skill to generate API calls and workflow guidance for creating short-form videos, grid videos, and slideshow carousel assets through lowkeyviral.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded images, and generated media are sent to lowkeyviral.com.

Mitigation: Use only content approved for that service and avoid sending sensitive or restricted material.

Risk: API requests can consume paid credits on the connected account.

Mitigation: Review generated commands and credit-cost steps before execution, especially image generation and render calls.

Risk: Brief deletion commands remove server-side resources.

Mitigation: Confirm the target brief ID and user intent before running delete requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tiotdev/skills/lowkey-viral)
- [Publisher profile](https://clawhub.ai/user/tiotdev)
- [lowkey viral homepage](https://github.com/tiotdev/lowkey-viral)
- [lowkey viral API keys](https://lowkeyviral.com/dashboard/api-keys)
- [lowkey viral API base](https://lowkeyviral.com/api/v1/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LOWKEY_VIRAL_API_KEY and curl; API calls may upload prompts, images, and generated assets to lowkeyviral.com and consume paid credits.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
