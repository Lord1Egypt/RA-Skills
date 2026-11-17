## Description:

Create and publish an Instagram carousel post from a tabiji.ai itinerary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Travel and social media operators use this skill to turn a tabiji.ai itinerary into an Instagram carousel by sourcing destination photos, applying text overlays, preparing a caption, and publishing through the Instagram Graph API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Instagram publishing credentials and publish content to an Instagram account.

Mitigation: Require an explicit human preview and approval of the target account, images, caption, and publish action before any Instagram API call is made.

Risk: The skill can make temporary carousel images publicly accessible and modify a GitHub repository.

Mitigation: Review the exact hosted image URLs and git changes before push, and remove temporary hosted images after publication is confirmed.

Risk: The security summary notes broad authority without clear approval gates or tight scoping.

Mitigation: Run the workflow with scoped credentials and repository access limited to the intended Instagram account and image-hosting path.

## Reference(s):

- [Instagram Graph API - Carousel Publishing Reference](references/instagram-graph-api.md)
- [ClawHub Skill Page](https://clawhub.ai/psyduckler/skills/itinerary-carousel-post)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the workflow creates temporary image files, a JSON image manifest, overlaid carousel slides, and an Instagram post URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
