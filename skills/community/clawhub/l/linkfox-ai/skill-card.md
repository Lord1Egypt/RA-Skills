## Description: <br>
LinkFoxAI lets an agent call the LinkFox AI Open Platform for image and video generation tasks, media upload, result polling, and documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, ecommerce operators, and agents use LinkFoxAI to submit LinkFox image and video generation jobs, upload image inputs, poll task status, and retrieve generated media URLs for product imagery, model scenes, sales videos, and related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires LinkFoxAI credentials and can send prompts, image URLs, and uploaded image files to LinkFox/Ziniao. <br>
Mitigation: Install only after approving that data flow, store LINKFOXAI_API_KEY securely, and avoid using sensitive local files or private media. <br>
Risk: The api-call command can call arbitrary documented LinkFox Open Platform paths under the configured base URL. <br>
Mitigation: Use api-call only for documented LinkFox AI endpoints and review request bodies before execution. <br>
Risk: Long-running generation and polling jobs may consume API quota or continue for many minutes. <br>
Mitigation: Use explicit timeouts, monitor spawned sessions, and stop or split jobs when results are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-ai) <br>
- [LinkFox AI Open Platform Access and Errors](references/open-platform.md) <br>
- [AI Image and Video API Reference](references/image-make.md) <br>
- [Ziniao Open Platform](https://open.ziniao.com) <br>
- [LinkFox Team API Guide](https://www.linkfox.com/team/api-guide) <br>
- [Open Platform API Call Guide](https://open.ziniao.com/docSupport?docId=233) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return task IDs, status or error objects, generated media URLs, and polling progress for long-running jobs.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
