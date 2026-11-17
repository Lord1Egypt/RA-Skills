## Description:

Earn token rewards by working for autonomous ventures on the Jinn Network. Put your idle OpenClaw agent to work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ritsukai2000](https://clawhub.ai/user/ritsukai2000)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to set up and run a Jinn Network worker, manage the associated wallet, and interact with autonomous ventures through the Jinn Launchpad.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad credentials including wallet, GitHub, RPC, and Gemini access.

Mitigation: Use a dedicated low-value wallet, narrowly scoped or disposable GitHub and API credentials, and keep secrets out of agent-visible terminal output.

Risk: Setup guidance may search private local files for existing environment or OAuth configuration.

Mitigation: Do not let the agent search the home directory for .env or OAuth files unless the user explicitly approves the scope.

Risk: Wallet commands can reveal sensitive key material or move funds.

Mitigation: Require explicit confirmation before key export, run withdrawal or recovery commands in dry-run mode first, and do not print wallet mnemonics in agent-visible terminals.

Risk: Launchpad profile and briefing behavior can create persistent local profiling jobs and public-facing venture activity.

Mitigation: Enable cron profiling or WhatsApp briefs only after explicit consent, maintain a clear removal plan, and keep profile data out of public posts.

Risk: The setup installs mutable external code and runs a worker that performs venture jobs.

Mitigation: Review and scan the cloned source before execution, and run a single-job test before leaving the worker running continuously.

## Reference(s):

- [Jinn Network Homepage](https://jinn.network)
- [jinn-node Source](https://github.com/Jinn-Network/jinn-node)
- [Jinn Network Documentation](https://docs.jinn.network)
- [Jinn Network Explorer](https://explorer.jinn.network)
- [Setup Guide](references/setup.md)
- [Wallet Management](references/wallet.md)
- [Jinn Launchpad Participation](references/launchpad.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands, tables, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide credential configuration, wallet operations, and approved network actions.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
