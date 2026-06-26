## Description: <br>
GPT-image2 uses the RedFox API to submit gpt-image-2 text-to-image and image-to-image jobs and download PNG, JPEG, or WebP outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, content marketers, e-commerce operators, and developers use this skill to generate or edit images from prompts and local reference images through the RedFox gpt-image-2 service, with controls for size, format, background, batch count, quality, and output location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected reference images, and the RedFox API key are sent to an external RedFox service for processing. <br>
Mitigation: Avoid private photos, confidential designs, regulated data, and secrets unless RedFox privacy and retention terms have been reviewed. <br>
Risk: The RedFox API key can be exposed if it is hardcoded, passed casually in commands, logged, or stored in an unprotected file. <br>
Mitigation: Prefer an environment variable or protected config file, avoid plaintext exposure in prompts, logs, code, and output files, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/image-gen-redfox) <br>
- [README.en.md](README.en.md) <br>
- [SKILL.md](SKILL.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox service](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated image files are PNG, JPEG, or WebP.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompts up to 500 characters, one to ten images, whitelisted image sizes, optional reference image upload, and RedFox API-key configuration.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
