## Description: <br>
Generates images with Amazon Nova Canvas through AWS Bedrock, using configured AWS credentials and command-line options for size, count, quality, seed, and negative prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wujiaming88](https://clawhub.ai/user/wujiaming88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to generate new images, illustrations, posters, icons, banners, or similar visual content through AWS Bedrock when they have Nova Canvas enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using AWS Bedrock/Nova Canvas can incur AWS charges. <br>
Mitigation: Install and run the skill only with an intended AWS account and confirm Bedrock access before generation. <br>
Risk: AWS secrets may be exposed if access keys are placed directly in prompts or command lines. <br>
Mitigation: Prefer an AWS profile, SSO, or a least-privilege role instead of passing access keys directly. <br>
Risk: Generated files may overwrite existing files at the selected output path. <br>
Mitigation: Choose explicit, non-conflicting output paths before running image generation. <br>


## Reference(s): <br>
- [Nova Canvas ClawHub listing](https://clawhub.ai/wujiaming88/nova-canvas) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AWS Bedrock access with Nova Canvas enabled; default output path is output.png, and multi-image runs save numbered files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
