## Description: <br>
Comprehensive Meitu AI toolkit for image and video editing, including poster design, background cutout, virtual try-on, e-commerce product workflows, video generation and editing, audio generation, text generation, and CLI-routed Meitu OpenAPI tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meituskills](https://clawhub.ai/user/meituskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill pack to route creative media requests to Meitu OpenAPI through scene-specific workflows and validated Meitu CLI commands. It supports image, video, audio, and text generation or editing tasks that require Meitu credentials and may produce local media outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill pack requires Meitu API credentials and can read credentials from environment variables or a local credentials file. <br>
Mitigation: Use environment variables where possible, restrict any credentials file permissions, and never commit credentials to version control. <br>
Risk: User media, prompts, and selected project, profile, or memory context may be sent to Meitu OpenAPI for processing. <br>
Mitigation: Avoid sensitive private photos, client data, or confidential project context unless the operator is permitted to send that data to Meitu OpenAPI. <br>
Risk: Some workflows can write local outputs, project metadata, or visual memory files. <br>
Mitigation: Review or disable memory and project-mode writes when durable profile, preference, DESIGN.md, or shared visual-memory changes are not desired. <br>


## Reference(s): <br>
- [ClawHub Meitu Skills release page](https://clawhub.ai/meituskills/meitu-skills) <br>
- [README](artifact/README.md) <br>
- [Security Model](artifact/SECURITY.md) <br>
- [Routing Guide](artifact/references/routing-guide.md) <br>
- [Task ID Baseline](artifact/references/task-id-baseline.md) <br>
- [Meitu Tools Skill](artifact/meitu-tools/SKILL.md) <br>
- [Meitu Tools Command Catalog](artifact/meitu-tools/references/tools.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON command results from the Meitu CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference generated or edited media files, task IDs, downloaded file paths, media URLs, and user-facing error guidance.] <br>

## Skill Version(s): <br>
2.0.12 (source: server release evidence and PACKAGE_MANIFEST.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
