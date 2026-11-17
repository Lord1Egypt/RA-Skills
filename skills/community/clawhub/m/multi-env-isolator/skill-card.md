## Description:

Generate isolated dev, test, and production environments for uvicorn/FastAPI Python web projects with Vue or React frontend support, including config files, startup scripts, data directories, Playwright test integration, and setup documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rm-huang](https://clawhub.ai/user/rm-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to scaffold separated dev, test, and production environments for FastAPI/uvicorn projects, including optional Vue or React frontend scripts and Playwright E2E test setup. It is suited for projects where development, QA, and production workflows need isolated ports, config, data, and startup commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill generates executable backend, frontend, and Playwright scripts that run local commands such as uvicorn, npm, and npx.

Mitigation: Use only on trusted local projects, inspect generated scripts before running them, and review npm package and lock files before frontend or Playwright execution.

Risk: Generated production configuration includes placeholder JWT secrets and local default settings.

Mitigation: Replace generated JWT secrets with strong random values, verify production CORS origins, keep DEBUG disabled, and confirm rate limiting before production use.

Risk: Command-line values are incorporated into generated project files and scripts.

Mitigation: Avoid untrusted command-line values and review generated environment files, documentation, and shell scripts before committing or executing them.

## Reference(s):

- [Configuration Options Reference](artifact/references/config-options.md)
- [ClawHub skill page](https://clawhub.ai/rm-huang/skills/multi-env-isolator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated Python, shell-script, environment-file, Playwright, and project documentation artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local project files and executable scripts for backend, frontend, and test workflows.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
