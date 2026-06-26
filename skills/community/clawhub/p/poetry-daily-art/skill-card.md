## Description: <br>
Generate daily Chinese classical poetry art cards by pairing an AI-generated landscape image with poem text and delivering the result to chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lava-lake](https://clawhub.ai/user/lava-lake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal automation agents use this skill to create a daily Chinese classical poetry image card, including poem selection, image generation, caption formatting, and chat delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends poetry-derived prompts to the MiniMax mmx image service. <br>
Mitigation: Install only if that third-party service is acceptable for the intended workflow and use a dedicated API key when possible. <br>
Risk: The generation script uses hardcoded local workspace paths. <br>
Mitigation: Review and adapt paths before running the script in a new environment. <br>
Risk: The script deletes prior image_*.jpg and image_*.png files in its output directory before generating a new image. <br>
Mitigation: Preserve any generated images that should be retained before running the script. <br>
Risk: Cron or chat delivery can create automatic daily messages. <br>
Mitigation: Enable scheduled execution or chat delivery only for channels where automatic posting is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lava-lake/poetry-daily-art) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command output and chat caption text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce a local image file path for media delivery when the MiniMax mmx CLI is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
