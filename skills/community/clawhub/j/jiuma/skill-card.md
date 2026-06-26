## Description: <br>
Jiuma AI Video Generation (Free) helps agents use Jiuma's media generation service to create videos, images, sounds, action imitation outputs, and character replacement results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[github-gamma](https://clawhub.ai/user/github-gamma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to authorize with Jiuma, upload media assets, submit AI media generation tasks, and retrieve generated media URLs and task status as JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected photos, videos, audio, prompts, and task data are sent to Jiuma's API. <br>
Mitigation: Avoid uploading confidential or identity-sensitive media unless the user accepts the provider-side privacy risk. <br>
Risk: A Jiuma authorization token is stored in the user's system keyring. <br>
Mitigation: Authorize intentionally, re-authorize only when needed, and remove stored credentials if access should be revoked. <br>
Risk: The upload helper sends the local file path provided by the user to Jiuma. <br>
Mitigation: Check file paths carefully before upload and only submit files selected for generation. <br>


## Reference(s): <br>
- [Jiuma website](https://www.jiuma.com) <br>
- [ClawHub skill page](https://clawhub.ai/github-gamma/jiuma) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task results may include generated media URLs, task identifiers, task status, and uploaded file URLs.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
