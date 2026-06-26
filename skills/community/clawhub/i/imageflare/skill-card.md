## Description: <br>
ImageFlare helps agents generate and edit images through the imageflare CLI using Cloudflare Workers AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sallytion](https://clawhub.ai/user/Sallytion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use ImageFlare to configure Cloudflare Workers AI credentials, generate images from text prompts, and edit existing images from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an unintended or untrusted pip package could execute unwanted code. <br>
Mitigation: Verify that the imageflare pip package is the intended package before installation. <br>
Risk: Cloudflare credentials stored in local configuration could grant unwanted access if exposed. <br>
Mitigation: Use a Cloudflare token limited to Workers AI, avoid putting tokens in shell history, and protect the local config file. <br>
Risk: Prompts and uploaded images are processed by Cloudflare Workers AI. <br>
Mitigation: Do not submit confidential prompts or sensitive images unless Cloudflare processing is acceptable for the use case. <br>


## Reference(s): <br>
- [ImageFlare ClawHub page](https://clawhub.ai/Sallytion/imageflare) <br>
- [Cloudflare Workers AI documentation](https://developers.cloudflare.com/workers-ai/) <br>
- [ImageFlare project homepage](https://github.com/Sallytion/Imageflare) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with shell command examples and PNG image file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the imageflare CLI, Cloudflare Workers AI credentials, and external Cloudflare processing; generated images are saved as PNG files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
