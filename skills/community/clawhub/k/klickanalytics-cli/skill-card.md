## Description:

Demonstrates and teaches the KlickAnalytics CLI, including market analytics commands, JSON-oriented agent integration patterns, and examples for financial research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klickanalytics](https://clawhub.ai/user/klickanalytics)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, and agent builders use this skill to learn how to install and call the KlickAnalytics CLI for financial markets research, automation, and JSON-based tool integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an external Python package that may change outside the skill artifact.

Mitigation: Install only when KlickAnalytics is trusted, prefer a dedicated virtual environment, and pin a reviewed package version where possible.

Risk: The setup instructions persist an API key in shell startup files, which can expose secrets on shared, synced, backed-up, or source-controlled machines.

Mitigation: Use a secret manager or tightly scoped environment injection rather than storing the API key directly in shell startup files.

## Reference(s):

- [KlickAnalytics CLI intro](https://www.klickanalytics.com/cli_intro)
- [KlickAnalytics CLI documentation](https://www.klickanalytics.com/cli_documentation)
- [KlickAnalytics CLI playground](https://www.klickanalytics.com/cli_playground)
- [OpenClaw integration guide](https://www.klickanalytics.com/cli_integration)
- [KlickAnalytics CLI changelog](https://www.klickanalytics.com/cli_changelog)
- [KlickAnalytics CLI command reference](references/commands.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands, code snippets, command examples, and JSON-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on the KLICKANALYTICS_CLI_API_KEY environment variable and CLI commands that commonly return JSON.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
