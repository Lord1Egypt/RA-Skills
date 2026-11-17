## Description:

Install and use OpenBoardCLI with `npm install -g openboard-cli` to turn Gmail receipts or CSV, Excel, and JSON data into authenticated React spending dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syedateebulislam](https://clawhub.ai/user/syedateebulislam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install, verify, configure, and operate OpenBoardCLI for generating authenticated React spending dashboards from Gmail receipts or CSV, Excel, and JSON data. It helps users choose local, hybrid, or remote operation modes while handling prerequisites and credential boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A global npm install can execute package installation behavior and affect the user's command environment.

Mitigation: Install only after trusting the OpenBoardCLI npm package and publisher, avoid administrator installs, and verify `openboard --version` and `openboard --help` before use.

Risk: Receipt, invoice, and dashboard data may include sensitive financial information.

Mitigation: Prefer local-only mode when data should not leave the machine and explain data boundaries before choosing local, hybrid, or all-remote operation.

Risk: Remote operation can require credentials for GitHub, Vercel, Gmail, dashboard access, or LLM providers.

Mitigation: Use environment variables for secrets, avoid logging tokens or passwords, and do not place credentials directly in command examples.

Risk: The live agent command contract may change over time.

Mitigation: Review the current command reference before following commands that use credentials, transmit data, or depend on exact flags.

## Reference(s):

- [OpenBoardCLI website and quickstart](https://openboard-site.vercel.app/)
- [OpenBoardCLI agent command contract](https://openboard-site.vercel.app/llms.txt)
- [OpenBoard repository](https://github.com/syedateebulislam/openboard)
- [OpenBoard full agent reference](https://github.com/syedateebulislam/openboard/blob/main/Agent.md)
- [ClawHub skill page](https://clawhub.ai/syedateebulislam/skills/openboard-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup checks, installation commands, operating-mode guidance, and credential-handling recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
