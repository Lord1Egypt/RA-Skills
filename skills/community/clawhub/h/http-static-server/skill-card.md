## Description: <br>
Start an ad-hoc HTTP static file server in the current directory using one-line commands across 25+ languages and tools. Auto-detects available runtimes and recommends the best option. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FlowerWrong](https://clawhub.ai/user/FlowerWrong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to quickly serve a local directory over HTTP for static-site previews, LAN file sharing, frontend asset testing, or lightweight development workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Serving the current directory can expose unintended local files, especially when bound to a LAN address. <br>
Mitigation: Serve a dedicated non-sensitive directory, prefer localhost or 127.0.0.1, and use 0.0.0.0 only when LAN access is intentional. <br>
Risk: Suggested options such as uploads, directory browsing, CORS, or Docker port publishing can broaden exposure. <br>
Mitigation: Review each command before use and enable those options only for a specific, understood need. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FlowerWrong/http-static-server) <br>
- [Big list of HTTP static server one-liners](https://gist.github.com/willurd/5720255) <br>
- [README](README.md) <br>
- [Python HTTP Static Server](references/python.md) <br>
- [Node.js HTTP Static Server](references/nodejs.md) <br>
- [Docker HTTP Static Server](references/docker.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and short decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be reviewed before execution and adjusted for the target port, directory, bind address, and installed runtime.] <br>

## Skill Version(s): <br>
2026.3.10 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
