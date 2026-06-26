## Description: <br>
加豆AI is an enterprise AIGC marketing and account-operations skill for generating short videos, digital-human presentations, commercial product images, model try-on images, product-scene images, video translation, lip-sync videos, and content for domestic and international social media accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiadouai](https://clawhub.ai/user/jiadouai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketing operators use this skill to configure ClawAgent access, submit AIGC media-generation jobs, upload local media when needed, poll job status, and manage supported social-media publishing or account workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill under-discloses sensitive file, token, and account-impacting behaviors. <br>
Mitigation: Review before installing, use a dedicated revocable token, verify every local file path before upload, avoid submitting confidential prompts or private media, and require explicit approval before publishing or account-management actions. <br>
Risk: The skill can upload local files to cloud storage for downstream media-generation tools. <br>
Mitigation: Confirm that each file is intended for upload, publicly shareable for the task, and free of private or regulated content before invoking upload workflows. <br>
Risk: Unsupported feature reporting can include the user's original prompt. <br>
Mitigation: Avoid entering secrets, private customer data, or confidential campaign details in prompts when using unsupported or exploratory requests. <br>


## Reference(s): <br>
- [加豆AI homepage](https://www.jiadouai.com) <br>
- [ClawHub skill page](https://clawhub.ai/jiadouai/jiadouai) <br>
- [AI commercial photography reference](references/ai_design.md) <br>
- [Authentication reference](references/auth.md) <br>
- [Common workflows reference](references/workflows.md) <br>
- [Unsupported feature reporting reference](references/unsupported_feature_reporting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include generated media URLs, job-status summaries, configuration steps, and error-handling guidance returned through ClawAgent tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
