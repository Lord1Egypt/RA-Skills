## Description: <br>
Design, debug, and harden GitHub Actions workflows with reusable pipelines, safe permissions, and faster CI and release automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to design, debug, secure, and optimize GitHub Actions workflows for CI, releases, and deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow edits or live run controls can affect repositories, releases, and deployments. <br>
Mitigation: Review proposed workflow changes and commands before execution, keep branch protections and environment approvals in place, and require explicit approval for deployment-impacting actions. <br>
Risk: Live inspection can send repository metadata, workflow files, run details, artifacts, and deployment payloads to GitHub or configured deployment endpoints. <br>
Mitigation: Use only approved repositories and endpoints, avoid pasting raw tokens or cloud keys into chat, and prefer GitHub secrets, protected environments, and OIDC for credentials. <br>
Risk: Configured maintainer or review automation may affect public repository content or share diffs with reviewer tools. <br>
Mitigation: Review moderation, autoreview, and maintainer workflows before use and limit them to trusted repositories and configured reviewers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/github-actions) <br>
- [Skill Homepage](https://clawic.com/skills/github-actions) <br>
- [Setup](artifact/setup.md) <br>
- [Workflow Patterns](artifact/workflow-patterns.md) <br>
- [Security Model](artifact/security-model.md) <br>
- [Debugging Playbook](artifact/debugging-playbook.md) <br>
- [Release Patterns](artifact/release-patterns.md) <br>
- [Performance Tuning](artifact/performance-tuning.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workflow drafts, review findings, debugging steps, release plans, and local memory templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
