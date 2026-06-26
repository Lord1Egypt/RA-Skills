## Description: <br>
Deploy frontend and full-stack projects to IGA Pages, including CLI-driven deploy, preview, build, link, login, and API route development workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seasonrui](https://clawhub.ai/user/seasonrui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to prepare, authenticate, build, and deploy frontend or full-stack projects to IGA Pages, and to add file-system based Node.js serverless API routes. It is most relevant when the user explicitly asks to publish a site, create a preview deployment, deploy to IGA Pages, or build an API endpoint for that platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route broad deployment or API requests into IGA Pages workflows even when the target platform is ambiguous. <br>
Mitigation: Confirm that the user intends to deploy to IGA Pages and that the project framework is supported before running IGA Pages CLI commands. <br>
Risk: Headless login instructions may lead users to pass cloud access keys directly in shell commands. <br>
Mitigation: Prefer browser login where available, avoid exposing long-lived access keys in chat or command history, and use least-privilege credentials when key-based login is necessary. <br>
Risk: Preview URLs can include query tokens that grant access. <br>
Mitigation: Treat preview URLs containing tokens as private access links and share them only with intended recipients. <br>


## Reference(s): <br>
- [Serverless Functions (API Routes)](artifact/references/functions.md) <br>
- [Volcengine IAM key management](https://console.volcengine.com/iam/keymanage) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include deployment URLs, including private preview URLs with query tokens when emitted by the IGA Pages CLI.] <br>

## Skill Version(s): <br>
1.0.5 (source: evidence release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
