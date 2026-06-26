## Description: <br>
AppVeyor helps agents query AppVeyor CI/CD data through OOMOL's AppVeyor connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect AppVeyor projects, build job artifacts, deployment environments, team roles, and team users through a connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting AppVeyor through OOMOL and can read AppVeyor projects, users, roles, environments, and build artifacts. <br>
Mitigation: Grant only the AppVeyor token scopes needed for the intended read-only queries and use an account appropriate for CI/CD visibility. <br>
Risk: Build artifacts and team metadata may contain sensitive project or organization information. <br>
Mitigation: Request only the specific project, build job, role, environment, or user data needed for the task and avoid sharing connector results outside the intended context. <br>
Risk: First-time setup may require installing or authenticating the oo CLI. <br>
Mitigation: Use only OOMOL's documented CLI installation source and run authentication or connection steps only after a command fails with the matching setup error. <br>


## Reference(s): <br>
- [AppVeyor homepage](https://www.appveyor.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [AppVeyor skill on ClawHub](https://clawhub.ai/oomol/oo-appveyor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before running actions; action responses include data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
