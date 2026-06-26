## Description: <br>
Generate high-quality images through Picnow for text-to-image and image-to-image workflows, including product photos, posters, banners, illustrations, covers, thumbnails, style transfer, background changes, and edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeekchen](https://clawhub.ai/user/jeekchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate or edit images from an agent by collecting image parameters, invoking the Picnow script, and returning generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to the external Picnow API provider. <br>
Mitigation: Do not submit secrets, private documents, regulated data, or sensitive personal images unless the provider's terms and privacy practices are acceptable. <br>
Risk: The skill requires a LETMEGO_API_KEY token for API access. <br>
Mitigation: Store the token in the environment and avoid placing it in prompts, generated files, shell history, or shared logs. <br>
Risk: Generated results are returned as public CDN URLs. <br>
Mitigation: Review image URLs before sharing or embedding them, especially for private or customer-sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeekchen/picnow) <br>
- [Picnow install and usage docs](https://picnow.letmego.top/skills) <br>
- [Picnow API provider](https://api.letmego.top) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown guidance with shell commands and JSON URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generation script prints a single JSON line containing image URLs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
