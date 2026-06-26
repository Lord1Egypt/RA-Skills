## Description: <br>
Media Gen helps agents generate AI images or videos through AIsa for creative drafts, media assets, and quick generation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request AIsa-backed image or video generation, create draft media assets, and run quick creative media workflows from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AISA_API_KEY authorizes AIsa-backed media-generation requests. <br>
Mitigation: Use a scoped or limited API key where possible and avoid exposing the key in prompts, shared logs, or generated output. <br>
Risk: Prompts and media-generation requests are sent to AIsa. <br>
Mitigation: Install and use the skill only when the requester trusts AIsa with the submitted prompts and generation requests. <br>
Risk: Generated media may be downloaded from service-returned URLs and saved locally. <br>
Mitigation: Choose output paths deliberately and review saved files before reuse or redistribution. <br>


## Reference(s): <br>
- [ClawHub Media Gen listing](https://clawhub.ai/bibaofeng/media-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell command examples, plus JSON command responses and generated media files from the bundled client.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY. Generated media may be saved to user-selected local output paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
