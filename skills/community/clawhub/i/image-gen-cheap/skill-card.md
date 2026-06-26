## Description: <br>
Generates and edits images through the LaoZhang API, supporting text-to-image prompts, image editing, multiple image models, URL outputs, and local image saves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enihsago](https://clawhub.ai/user/enihsago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate new images from prompts or edit source images through LaoZhang API-backed image models from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and source image URLs are sent to LaoZhang's external API. <br>
Mitigation: Do not use private images, confidential business material, secrets, regulated data, or private/internal URLs unless that sharing is approved. <br>
Risk: The skill reads a LaoZhang API token from ~/.laozhang_api_token or a command-line argument. <br>
Mitigation: Treat the token like a password; keep it out of shared folders, repositories, logs, and generated artifacts. <br>
Risk: Generated image outputs may contain sensitive content depending on prompts and inputs. <br>
Mitigation: Review generated outputs before sharing or storing them in collaborative or public locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/enihsago/image-gen-cheap) <br>
- [LaoZhang API registration](https://api.laozhang.ai/register/?aff_code=lfa0) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, API responses, image URLs, and saved image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LaoZhang API token; generated images may be returned as URLs or base64 and can be saved locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
