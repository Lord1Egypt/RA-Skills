## Description: <br>
Glasses to Social helps an agent monitor a Google Drive folder for smart-glasses photos, analyze new images with vision AI, draft social posts in the user's voice, and publish only after approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Junebugg1214](https://clawhub.ai/user/Junebugg1214) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, developers, and social media operators use this skill to build a smart-glasses photo workflow that turns new images into AI-drafted captions and approval-gated social posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Photos in the monitored folder may include sensitive content or bystanders who did not consent to social posting. <br>
Mitigation: Use a dedicated Google Drive folder, avoid adding sensitive or bystander photos without consent, and review the AI provider's image-retention policy before processing images. <br>
Risk: Drafted captions or selected images could be published unintentionally. <br>
Mitigation: Keep auto-posting disabled and require manual approval of every image preview and caption before anything is posted. <br>
Risk: Vision analysis may produce inaccurate or misleading context for a social post. <br>
Mitigation: Review and edit each generated caption against the source image before approving publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Junebugg1214/glasses-to-social) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and draft social post text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires manual approval before publishing and tracks processed photos in a JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
