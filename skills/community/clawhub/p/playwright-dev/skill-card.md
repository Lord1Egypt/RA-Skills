## Description: <br>
Provides agent guidance and a Python helper script for generating or editing images with Nano Banana Pro, using Gemini 3 Pro Image with optional input images and 1K, 2K, or 4K output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to create new images or edit existing images from prompts, while producing repeatable shell commands and saved PNG output files in the user's working directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package contains broad personal automation, credential, messaging, memory, scheduled-task, and gateway configuration files that do not fit the advertised image-generation purpose. <br>
Mitigation: Review before installation and reduce the release to the purpose-aligned skill instructions and image-generation script. <br>
Risk: Exposed API keys or messaging tokens may be present in the package. <br>
Mitigation: Rotate any exposed credentials or messaging tokens before use and avoid installing the untrimmed package into a normal agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icesumer-lgtm/playwright-dev) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Image generation script](artifact/clawhub skills/scripts/generate_image.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; the helper script prints status text and saves PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompt text, optional input-image path, filename, API key, and 1K, 2K, or 4K resolution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
