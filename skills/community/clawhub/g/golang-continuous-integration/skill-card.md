## Description:

CI/CD pipeline configuration using GitHub Actions for Go projects, including testing, linting, SAST, security scanning, coverage, dependency automation, GoReleaser workflows, code review automation, and release pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to set up or improve GitHub Actions CI/CD for Go projects. It guides agents in producing workflow files, release and dependency automation configuration, security scanning setup, and review guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI review workflow can add persistent automation with broad GitHub permissions and mutable remote installs.

Mitigation: Review or remove the AI review workflow before installation; pin npx packages, GitHub Actions, Go tooling, and fetched skill repositories to immutable versions; restrict AI review triggers to trusted contributors.

Risk: Review jobs may process untrusted PR files, comments, diffs, and logs.

Mitigation: Treat PR-supplied content as untrusted, avoid posting raw workflow log excerpts to PRs, remove unnecessary id-token write permissions from review jobs, and scope actions read permissions narrowly.

Risk: Release, Docker publishing, and auto-merge workflows can modify repository state, publish artifacts, or use secrets.

Mitigation: Require branch protection, required status checks, approvals, least-privilege workflow permissions, and careful secret management before enabling these workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-continuous-integration)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Repository security settings](artifact/references/repo-security.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML workflow templates and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify GitHub Actions workflows, GoReleaser files, dependency automation configuration, and review instructions.]

## Skill Version(s):

1.4.0 (source: server release metadata, SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
