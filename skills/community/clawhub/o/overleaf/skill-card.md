## Description: <br>
Access Overleaf projects via CLI. Use for reading/writing LaTeX files, syncing local .tex files to Overleaf, downloading projects, managing Overleaf project structure, and accepting project invitations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and writing teams use this skill to let an agent read, edit, sync, download, and manage LaTeX projects in Overleaf through pyoverleaf and authenticated browser sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on pyoverleaf access to browser cookies and keychain-protected session data. <br>
Mitigation: Install only after reviewing and pinning the pyoverleaf version, and prefer a dedicated browser profile or separate Overleaf account. <br>
Risk: The skill can modify, delete, sync, download, or accept invitations for Overleaf projects using the logged-in session. <br>
Mitigation: Require explicit user confirmation before write, delete, sync, download, or invite-acceptance actions. <br>


## Reference(s): <br>
- [ClawHub Overleaf Skill](https://clawhub.ai/EasonC13/overleaf) <br>
- [pyoverleaf GitHub Repository](https://github.com/jkulhanek/pyoverleaf) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands or snippets that read, write, delete, download, sync, or accept invitations for Overleaf projects.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
