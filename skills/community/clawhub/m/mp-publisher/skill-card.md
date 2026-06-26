## Description: <br>
Automates a WeChat public-account article workflow from topic selection through drafting, review, image generation, and creation of account drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuxixixi](https://clawhub.ai/user/wuxixixi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams and developers use this skill to coordinate WeChat public-account article production, including topic generation, article drafting, quality review, supporting image generation, and draft creation in the official account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored WeChat public-account credentials and a DMX image API key can be used to create external drafts or generate images. <br>
Mitigation: Use dedicated or low-risk credentials, keep secrets out of shared logs, and verify the configured DMX endpoint before running the workflow. <br>
Risk: Broad chat triggers may start external draft creation without a clearly documented final approval step. <br>
Mitigation: Manually review generated topics, article content, images, and draft status before publishing anything publicly. <br>
Risk: The WeChat API test command prints part of an access token in logs. <br>
Mitigation: Avoid sharing command output or logs from credential tests and rotate credentials if token fragments are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuxixixi/mp-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles, plain-text workflow status, configuration snippets, and command-line instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create generated image files and WeChat public-account drafts when configured credentials and external APIs are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
