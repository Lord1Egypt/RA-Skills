## Description: <br>
Recognizes objects, scenes, text, faces, plants, animals, products, landmarks, and other content in local, URL, or Base64 images using Baidu AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ide-rea](https://clawhub.ai/user/ide-rea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit local images, image URLs, or Base64 images for general Baidu AI image understanding and Markdown summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, image URLs, and derived recognition results are sent to Baidu. <br>
Mitigation: Use only images that are appropriate to share with Baidu, and avoid sensitive photos or private/internal URLs. <br>
Risk: The skill requires a Baidu API key and may reuse credentials from prior chat context. <br>
Mitigation: Use a restricted Baidu API key, prefer environment-provided credentials, and confirm any pasted key is intended for this skill before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ide-rea/image-recognize) <br>
- [Baidu Qianfan service](https://qianfan.baidubce.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown recognition report with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts local image paths, image URLs, or Base64 image data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
