## Description: <br>
Nano Banana Pro Cn helps agents generate and edit images through APIYI's NanoBananaPro image service, supporting text-to-image, image-to-image, multiple aspect ratios, and 1K, 2K, or 4K outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to create new images or edit selected local images, then run the included Node.js or Python command-line tool with the desired prompt, output path, aspect ratio, and resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to APIYI for processing. <br>
Mitigation: Use the skill only for content that is acceptable to share with APIYI, and avoid confidential or regulated images unless APIYI's terms and retention practices are acceptable. <br>
Risk: Passing an API key on the command line can expose the key through shell history or process listings. <br>
Mitigation: Prefer the APIYI_API_KEY environment variable and use a dedicated API key for this skill. <br>


## Reference(s): <br>
- [Common Usage Scenarios](references/scene.md) <br>
- [APIYI](https://apiyi.com/) <br>
- [APIYI API Console](https://api.apiyi.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with command-line examples; generated or edited PNG image files are saved locally.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an APIYI_API_KEY environment variable or command-line API key and may use optional input images, aspect ratio, resolution, and output filename parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
