## Description: <br>
Mj Gallery generates MXAI MJ images from text prompts, downloads them locally, archives them in a web gallery, deploys the gallery, and returns accessible result links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate MJ-style images through MXAI, keep local image copies, and publish a lightweight gallery for sharing recent outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated images, prompt summaries, filenames, and task metadata may be saved in the workspace and published through the gallery link. <br>
Mitigation: Avoid confidential prompts, private reference images, client work, or other sensitive content unless the deployment destination is controlled and removable. <br>
Risk: The skill requires an MX_AI_API_KEY credential for image generation. <br>
Mitigation: Use a scoped or revocable API key and rotate it if it may have been exposed. <br>
Risk: Generated or referenced material may create ownership or copyright concerns when shared publicly. <br>
Mitigation: Use prompts and reference images only when you have the rights needed for the intended gallery publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/mj-gallery) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tianheihei002) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown response with local image paths, generated gallery files, and deployed gallery links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates WebP image files, updates a gallery index.html, and keeps the most recent 20 gallery entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
