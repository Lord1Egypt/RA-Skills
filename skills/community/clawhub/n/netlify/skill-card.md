## Description: <br>
Use the Netlify CLI to create and link Netlify sites, configure GitHub-backed CI/CD, set build and environment settings, and support monorepo deployment patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajmwagar](https://clawhub.ai/user/ajmwagar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create or connect Netlify sites, especially for GitHub-backed CI/CD and monorepo deployments with per-site build configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help run Netlify CLI actions that create, link, initialize, or deploy sites and therefore affect a Netlify account or production site. <br>
Mitigation: Confirm the target site folder, Netlify team or account, site name, GitHub repository, build settings, and production-deploy intent before running commands. <br>
Risk: A long-lived or overly broad Netlify token could increase account exposure if reused outside the intended workflow. <br>
Mitigation: Prefer a scoped Netlify token that can be revoked, and avoid storing credentials in skill files or generated configuration. <br>


## Reference(s): <br>
- [Netlify skill page](https://clawhub.ai/ajmwagar/netlify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Netlify configuration files and propose Netlify CLI commands for site, CI/CD, environment variable, and deployment workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-02-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
