## Description: <br>
Creates and publishes an Instagram carousel post from a tabiji.ai itinerary by sourcing destination photos, applying text overlays, and publishing via Instagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators, travel marketers, or operators of tabiji.ai social accounts use this skill to turn an itinerary URL, destination, attraction list, and optional caption into a six-slide Instagram carousel and published post URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public Instagram carousel posts using configured Instagram credentials. <br>
Mitigation: Require a final preview of images and caption, confirm the target Instagram account, and publish only with an approved token for that account. <br>
Risk: The workflow can push and later delete hosted carousel images in the tabiji GitHub repository. <br>
Mitigation: Use a dedicated repository path, inspect the git diff before push, and confirm cleanup changes before deleting hosted images. <br>
Risk: Destination titles, captions, and sourced photos can create rights, attribution, or content-quality issues. <br>
Mitigation: Sanitize user-provided titles and captions, verify image rights before publishing, and replace low-quality or unsuitable photos before API submission. <br>


## Reference(s): <br>
- [Instagram Graph API - Carousel Publishing Reference](references/instagram-graph-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown workflow with bash and curl examples, JSON manifest, JPEG carousel images, and Instagram post URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates temporary image files and may publish public Instagram content through configured Instagram and GitHub credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
