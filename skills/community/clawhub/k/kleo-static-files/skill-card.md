## Description: <br>
Host static files on subdomains with optional authentication for HTML, images, CSS, JavaScript, and other static content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awaaate](https://clawhub.ai/user/awaaate) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create static hosting sites, upload files or directories, configure basic authentication, inspect usage, and manage hosted content through the sf CLI or API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented quick install runs unpinned remote code as administrator. <br>
Mitigation: Review the installer before execution, pin it to a trusted commit where possible, or use the manual installation path on a test host first. <br>
Risk: The helper workflows can publish, overwrite, share, or delete hosted content. <br>
Mitigation: Require explicit confirmation before uploads, --overwrite, file or site deletion, clean-deploy, or sharing sensitive files. <br>
Risk: API credentials allow static hosting changes in the configured environment. <br>
Mitigation: Provide SF_API_KEY only in environments where the agent is authorized to modify hosted files and sites. <br>


## Reference(s): <br>
- [Installation Guide](references/install.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/awaaate/kleo-static-files) <br>
- [Bun Runtime](https://bun.sh) <br>
- [Caddy Web Server](https://caddyserver.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, configuration snippets, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose CLI or API actions that create, overwrite, publish, or delete hosted files and sites.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
