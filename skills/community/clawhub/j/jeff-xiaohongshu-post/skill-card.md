## Description: <br>
Creates Xiaohongshu-style post packages from a topic, audience, and core message, including researched title options, confirmed copy, hashtags, and a 3:4 cover image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and content operators use this skill to draft Xiaohongshu posts after confirming the title and outline, then produce publishing-ready copy, hashtags, and a vertical cover image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send the topic, audience, title, and image prompt to external search and image-generation services. <br>
Mitigation: Avoid sensitive or confidential inputs, review prompts before submission, and use narrowly scoped credentials for image generation. <br>
Risk: The recommended KIE image path exposes a local callback service through a public tunnel using helper scripts that were not included for review. <br>
Mitigation: Prefer the included Seedream path, or use the KIE tunnel only after reviewing the helper scripts and adding explicit authentication and shutdown controls. <br>
Risk: The skill requires sensitive credentials for image generation. <br>
Mitigation: Store credentials outside the skill artifact, rotate them regularly, and revoke them if the workspace or output files are shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffli2002/jeff-xiaohongshu-post) <br>
- [Seedream image generation endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown copy plus image files and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces title candidates, an outline for user confirmation, final post copy with hashtags, and cover image assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
