## Description: <br>
Tạo ảnh infographic, banner hoặc poster trực tiếp bằng một prompt gửi tới API tạo ảnh qua 9Router. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanminhhole](https://clawhub.ai/user/tuanminhhole) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to gather required infographic details from a user, compose a detailed image prompt, and run a local Node.js generator that creates Vietnamese infographic, poster, or banner images through 9Router. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive 9Router/OpenClaw API credentials and sends prompts to the configured 9Router endpoint. <br>
Mitigation: Install only when that credential and endpoint use is acceptable, verify the base URL, and scope credentials according to local policy. <br>
Risk: Image prompts can contain private or sensitive information. <br>
Mitigation: Keep prompts free of sensitive private data before invoking the generator. <br>
Risk: A chosen image output path could overwrite another file. <br>
Mitigation: Use a normal, intentional image output path and review the filename before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuanminhhole/infographic-generator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tuanminhhole) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands that produce image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images depend on the configured 9Router endpoint, selected image model, prompt detail, credentials, and output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
