## Description:

Use Parallel's parallel-cli to do live web search, URL extraction, deep research reports, bulk data enrichment, FindAll entity discovery, and web monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need current web research, URL extraction, cited reports, dataset enrichment, entity discovery, or web monitoring through Parallel's CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can install a dependency by running an internet-hosted shell script.

Mitigation: Prefer the documented pipx installation path, or independently review and verify the installer script before execution.

Risk: Search, extraction, enrichment, research, and monitoring send task data to Parallel's service.

Mitigation: Use the skill only with data approved for that service and avoid submitting confidential or sensitive information unless the deployment policy permits it.

Risk: Monitor webhooks can disclose results to external endpoints.

Mitigation: Configure webhooks only for endpoints the operator controls and trusts.

## Reference(s):

- [Parallel CLI documentation](https://docs.parallel.ai/integrations/cli)
- [Command templates](references/command-templates.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/parallel-ai-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and links, plus JSON or file outputs when Parallel CLI commands are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary research, extraction, enrichment, or monitoring result files when outputs are long-running or large.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
