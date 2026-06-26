## Description: <br>
Turns product photos or a store URL into a polished product video by relaying media and the user's brief to Pexo's hosted video service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pexo](https://clawhub.ai/user/pexo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create e-commerce product videos from product media or store URLs, monitor rendering progress, handle revisions, and return finished video asset links to users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends product photos, downloaded URL content, prompts, and project metadata to Pexo's hosted service. <br>
Mitigation: Use the skill only when sharing that media with Pexo is allowed by the user's confidentiality, privacy, and data-handling policies. <br>
Risk: The skill requires a Pexo API key and stores configuration in the user's Pexo config file. <br>
Mitigation: Treat the API key as a secret, restrict config-file permissions, and rotate the key if it is exposed. <br>
Risk: Video generation can consume Pexo credits or require credit purchases. <br>
Mitigation: Confirm the user is comfortable using credits before submitting jobs or retrying after credit-related errors. <br>


## Reference(s): <br>
- [Pexo](https://pexo.ai) <br>
- [Product Video Maker on ClawHub](https://clawhub.ai/pexo/product-video-maker) <br>
- [Setup Checklist](references/SETUP-CHECKLIST.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON script responses, project links, and plain text asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses asynchronous project polling and may return signed media URLs, local cached asset paths, status updates, and revision guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
