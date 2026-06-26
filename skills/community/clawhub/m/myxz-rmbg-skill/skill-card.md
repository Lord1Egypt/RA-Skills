## Description: <br>
妙言小智 (PicTech.cc) 专业级跨境电商图片抠图/白底图工具，帮助 agents 处理图片去背景、透明底图、白底图、纯色背景图、本地图片、网络图片、文件夹图片和批量抠图任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pictechai](https://clawhub.ai/user/pictechai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to remove or replace image backgrounds for cross-border e-commerce product imagery, including transparent PNGs, white-background marketplace images, custom solid backgrounds, and batch folder processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, including batch folder contents, are sent to the PicTech/stableai cloud service for processing. <br>
Mitigation: Use the skill only for images approved for that external processing flow, and avoid processing sensitive images unless the user accepts that transfer. <br>
Risk: Documentation examples and credential-memory claims may encourage unsafe VK/API-key handling. <br>
Mitigation: Configure the VK/API key through platform configuration or the RMBG_VK environment variable, avoid pasting keys into chat, and rotate any key that appears in prompts or logs. <br>
Risk: Processed outputs and cache files may remain on local storage after use. <br>
Mitigation: Review and delete local output and cache files when processing confidential or regulated images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pictechai/myxz-rmbg-skill) <br>
- [PicTech.cc website](https://www.pictech.cc) <br>
- [PicTech API service](https://stableai.com.cn) <br>
- [VK app key page](https://www.pictech.cc/newpictech/skills/openclaw-image-translation-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Text, Guidance] <br>
**Output Format:** [PNG image files plus a structured JSON execution result that can be summarized in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves processed images to a local output directory and may reuse local cached results for repeated inputs.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
