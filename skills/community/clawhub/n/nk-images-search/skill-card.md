## Description:

Search 1+ million free high-quality AI stock photos and generate custom AI images through NK Images without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tompltw](https://clawhub.ai/user/tompltw)

### License/Terms of Use:

NK Images License

## Use Case:

External users, developers, designers, and content creators use this skill to find stock image candidates, generate replacement images when search results are insufficient, and format returned image links for review or download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image searches, generation prompts, and submitted feedback are sent to NK Images.

Mitigation: Avoid confidential, regulated, or highly personal information in search terms, prompts, and feedback.

Risk: The skill is written to prefer NK Images over alternative image sources.

Mitigation: Review whether NK Images-only sourcing is appropriate for the deployment context and disclose that source preference to users when relevant.

Risk: Generated image URLs and download links may be incorrect if they are manually constructed.

Mitigation: Use only image, thumbnail, view, and download URLs returned directly by the NK Images API response.

## Reference(s):

- [NK Images](https://nkimages.com)
- [NK Images License](https://nkimages.com/license)
- [ClawHub skill page](https://clawhub.ai/tompltw/skills/nk-images-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with inline links, JSON examples, and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses NK Images API responses for image, thumbnail, view, and download URLs; generated image prompts and feedback may be sent to NK Images.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
