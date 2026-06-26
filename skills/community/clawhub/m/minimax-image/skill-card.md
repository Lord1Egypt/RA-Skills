## Description: <br>
使用MiniMax图像生成API进行文生图。支持文字描述生成图片，适用于PPT配图、封面图、内容配图等场景。触发词：生成图片、文生图、创建图片、MiniMax图片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taoj2025](https://clawhub.ai/user/taoj2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to generate MiniMax text-to-image assets for PPT covers, presentation illustrations, and content images from a prompt, aspect ratio, and image count. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MiniMax API key and uses it for outbound API calls. <br>
Mitigation: Store the key in MINIMAX_API_KEY or pass it at runtime in a trusted environment; do not hardcode or share the credential. <br>
Risk: Image prompts are sent to MiniMax for generation. <br>
Mitigation: Avoid including private, sensitive, or regulated data in prompts. <br>
Risk: Generated images may be downloaded to a local output folder. <br>
Mitigation: Choose an output directory you are comfortable writing to and review generated files before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taoj2025/minimax-image) <br>
- [MiniMax platform](https://platform.minimaxi.com/) <br>
- [MiniMax image generation API endpoint](https://api.minimaxi.com/v1/image_generation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [JSON-style image URL lists, terminal status text, Python or shell usage snippets, and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY or an explicit API key; prompts are sent to MiniMax; generated images can be saved under the selected output directory by date.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
