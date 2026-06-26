## Description: <br>
Generates AI-assisted presentation slide images from source content, with optional transition prompts, transition videos, interactive viewers, and full video export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ITRocker](https://clawhub.ai/user/ITRocker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and presentation authors use this skill to turn documents or pasted content into planned slide decks, generated slide images, and optional video presentation assets. It is intended for workflows where users can review generated content before sharing or publishing it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Source documents, generated slide images, and transition prompts may be sent to third-party AI providers for image or video generation. <br>
Mitigation: Use the skill only with data approved for those providers, and avoid confidential, regulated, customer-sensitive, or unpublished material unless provider use is authorized. <br>
Risk: API keys can be exposed if users paste real credentials into chat or commit local environment files. <br>
Mitigation: Configure keys locally in a protected .env file or secret manager, use limited-scope keys, keep .env out of version control, and rotate any key that was shared in a prompt. <br>
Risk: Generated presentations and videos can contain incorrect, misleading, or low-quality content. <br>
Mitigation: Review generated slide plans, images, videos, and viewer output before publication or external sharing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ITRocker/nanobanana-ppt-skills) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Architecture](artifact/ARCHITECTURE.md) <br>
- [Security Guidance](artifact/SECURITY.md) <br>
- [API Management](artifact/API_MANAGEMENT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON plans, shell commands, generated image/video files, and HTML viewers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create slides_plan.json, prompts.json, transition_prompts.json, PNG slide images, MP4 videos, and local HTML playback pages under an output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
