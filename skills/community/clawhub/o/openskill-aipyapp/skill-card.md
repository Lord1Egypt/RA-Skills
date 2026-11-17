## Description:

AIPyApp is an AI-driven Python automation skill that helps agents install and configure AIPyApp, then use natural-language instructions for web scraping, file processing, content conversion, and script execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riverfor](https://clawhub.ai/user/riverfor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to install and configure AIPyApp, then ask an agent to run Python-backed automation tasks such as web scraping, image processing, file conversion, and interactive or API-based execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and setup guidance can make system-wide Python package changes, including use of `--break-system-packages`.

Mitigation: Install in a virtual environment or with pipx, pin the `aipyapp` package version, and avoid running the installer as root unless system-level changes are intended.

Risk: The skill enables broad AI-generated code execution and automatic dependency installation.

Mitigation: Review generated scripts and dependencies before execution, constrain the working directory, and disable auto-install behavior unless it is required for the task.

Risk: LLM provider configuration requires API keys and includes result-sharing options in the sample configuration.

Mitigation: Keep API keys out of logs and generated files, store secrets in a managed secret store when possible, and disable result sharing unless explicitly needed.

## Reference(s):

- [AIPyApp configuration template](references/config.md)
- [ClawHub skill page](https://clawhub.ai/riverfor/skills/openskill-aipyapp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, TOML configuration examples, and generated Python automation behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install Python dependencies, invoke configured LLM providers, and execute generated automation scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
