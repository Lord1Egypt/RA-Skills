## Description: <br>
Securely clone GitHub projects with safety checks, dependency analysis, and security recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tugocoffe](https://clawhub.ai/user/tugocoffe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to clone GitHub repositories into a chosen directory, inspect project structure and dependency files, and receive safety-focused installation guidance before running code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloning or validation scripts may alter local files if run against an important target path. <br>
Mitigation: Use a fresh temporary directory and do not confirm overwrite prompts for paths that contain important work. <br>
Risk: Repository text, scripts, and dependency files are untrusted inputs and may include unsafe instructions. <br>
Mitigation: Inspect cloned content manually before execution and keep evaluation isolated from sensitive workspaces. <br>
Risk: Suggested pip or npm commands and alternate package indexes can introduce dependency or supply-chain risk. <br>
Mitigation: Review installation commands, package sources, and indexes before use, and prefer isolated virtual environments or containers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tugocoffe/github-installer-agent) <br>
- [GitHub Security Best Practices](https://docs.github.com/en/security) <br>
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices/) <br>
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html) <br>
- [npm Security Audit Guide](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities) <br>
- [Git Shallow Clone Documentation](https://git-scm.com/docs/git-clone#Documentation/git-clone.txt---depthltdepthgt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security analysis report with inline shell commands and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository metadata, project structure summaries, dependency previews, and safety warnings.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
