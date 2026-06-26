## Description: <br>
Uses OpenCLI to help an agent retrieve website and platform data, download media, control supported desktop apps, and route commands through external CLI tools across social, video, knowledge, finance, developer, and productivity services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wike-CHI](https://clawhub.ai/user/Wike-CHI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill when they need an agent to query supported web platforms, export or download media, automate local desktop applications, or invoke tools such as GitHub CLI, Docker, and kubectl through OpenCLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents access to logged-in browser sessions, desktop apps, downloads, and powerful local CLIs. <br>
Mitigation: Install only when OpenCLI, its browser extension, and reachable accounts or local tools are trusted; prefer a separate Chrome profile and non-production GitHub, Docker, and Kubernetes contexts. <br>
Risk: Commands may perform logged-in access, writes, deletes, publishing, downloads, desktop automation, or infrastructure-changing actions. <br>
Mitigation: Require explicit approval before running commands that change state, access authenticated data, download media, automate desktop applications, or modify infrastructure. <br>


## Reference(s): <br>
- [OpenCLI GitHub repository](https://github.com/jackwener/opencli) <br>
- [OpenCLI npm package](https://www.npmjs.com/package/@jackwener/opencli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and OpenCLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that access logged-in browser sessions, local desktop apps, downloads, and external CLI contexts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
