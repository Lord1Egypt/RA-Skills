## Description: <br>
Generate AI images from text prompts using a guided confirmation flow with optional reference image URLs, model, resolution, and aspect ratio choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xFANGO](https://clawhub.ai/user/0xFANGO) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate cover images, illustrations, concept art, or other visual assets from natural-language prompts through a confirmation-first workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and reference image URLs are sent to the Labnana provider. <br>
Mitigation: Avoid sensitive prompts, private image links, and tokenized URLs; review the confirmation summary before approving generation. <br>
Risk: The skill requires a ListenHub/Labnana API key. <br>
Mitigation: Provide LISTENHUB_API_KEY only in a trusted environment and do not paste secrets into prompts or saved prompt files. <br>
Risk: Generated images may be saved locally when download output is enabled. <br>
Mitigation: Review the configured output mode and inspect .listenhub/image-gen/ before sharing or retaining generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xFANGO/marswave-image-gen) <br>
- [Image Prompt Guide](references/prompt-guide.md) <br>
- [Labnana image generation API endpoint](https://api.labnana.com/openapi/v1/images/generation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, files] <br>
**Output Format:** [Markdown guidance with bash and JSON snippets; generated images are shown inline, saved as JPG files, or both depending on configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LISTENHUB_API_KEY and writes generated image files under .listenhub/image-gen/YYYY-MM-DD-{jobId}/ when download output is selected.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
