## Description: <br>
CI/CD pipeline configuration using GitHub Actions for Golang projects, including testing, linting, SAST, security scanning, code coverage, dependency automation, release pipelines, and AI-assisted code review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up or improve Go project CI/CD in GitHub Actions, including test, lint, security, dependency update, release, Docker, and AI review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled AI review workflow grants broad GitHub permissions and log access. <br>
Mitigation: Review the workflow before installation, remove unused id-token: write, limit actions: read to jobs that need logs, and restrict triggers to trusted contributors or protected branches. <br>
Risk: Full workflow output and repository logs can expose sensitive CI data if secrets or tokens are printed. <br>
Mitigation: Disable full output where possible, keep secrets in GitHub Secrets or protected environments, and verify workflows do not print sensitive values. <br>
Risk: Release, auto-merge, and package publishing workflows require elevated write permissions. <br>
Mitigation: Use branch protection, required checks, reviewer gates, least-privilege permissions, and scoped secrets before enabling automated merge or publishing paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-continuous-integration) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [Repository Security Settings](references/repo-security.md) <br>
- [Renovate GitHub App](https://github.com/apps/renovate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-specific GitHub Actions workflow files and related configuration guidance for Go repositories.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
