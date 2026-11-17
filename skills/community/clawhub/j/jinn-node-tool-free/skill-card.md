## Description:

节点工作工具 helps personal users run an agent-assisted worker node on idle machines to complete tasks and earn points rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External personal developers use this skill to initialize a single worker node, configure wallet-backed operation, run one-off or continuous tasks, and check wallet and completion records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented partly like a generic productivity tool while evidence.security describes it as a wallet-backed blockchain or node worker.

Mitigation: Use it only when intentionally setting up an agent-assisted node worker, and review the requested actions before running commands or staking-related steps.

Risk: The workflow may involve API keys, wallet passwords, local wallet material, and backup archives.

Mitigation: Keep .env contents, wallet passwords, backup archives, and tokens out of shared, logged, or CI environments; store wallet backups offline.

Risk: The skill may install packages, run long-lived worker commands, and perform staking-related wallet operations.

Mitigation: Run it in an isolated local environment, start with a single-task test run, verify balances and commands manually, and keep recoverable backups before continuous operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jinn-node-tool-free)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment-variable names, package installation commands, node operation commands, and wallet backup or recovery guidance.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
