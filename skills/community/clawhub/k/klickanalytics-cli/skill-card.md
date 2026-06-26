## Description: <br>
Demonstrates and teaches the KlickAnalytics CLI (`ka`) for financial markets intelligence, including command discovery, setup, automation examples, and agent or LLM integration patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klickanalytics](https://clawhub.ai/user/klickanalytics) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, quants, and agent builders use this skill to learn and apply KlickAnalytics CLI commands for market research, JSON-oriented automation, and LLM tool integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The KlickAnalytics CLI API key is sensitive and could be exposed through shell configuration, logs, shared terminals, or synced dotfiles. <br>
Mitigation: Treat `KLICKANALYTICS_CLI_API_KEY` like a password, prefer a local secret manager or private environment configuration, and avoid placing it in shared or synced files. <br>
Risk: `ka ai-chat` prompts may contain confidential financial research, credentials, account details, or regulated information. <br>
Mitigation: Avoid sending confidential or regulated information to `ka ai-chat` unless the user is comfortable with KlickAnalytics or its providers processing that content. <br>


## Reference(s): <br>
- [KlickAnalytics CLI command reference](references/commands.md) <br>
- [KlickAnalytics CLI intro](https://www.klickanalytics.com/cli_intro) <br>
- [KlickAnalytics CLI documentation](https://www.klickanalytics.com/cli_documentation) <br>
- [KlickAnalytics CLI playground](https://www.klickanalytics.com/cli_playground) <br>
- [OpenClaw integration guide](https://www.klickanalytics.com/cli_integration) <br>
- [KlickAnalytics CLI changelog](https://www.klickanalytics.com/cli_changelog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, and JSON-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exact `ka` commands and API-key setup guidance; the skill itself provides instructions and does not execute the CLI.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
