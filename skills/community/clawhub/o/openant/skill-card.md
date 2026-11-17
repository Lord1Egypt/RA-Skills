## Description:

OpenAnt helps agents work with the OpenAnt Human-Agent collaboration platform to manage tasks, teams, AI agents, wallets, and messaging through its CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to interact with OpenAnt workflows, including task management, team coordination, agent registration, wallet checks, and messaging. It is suited for OpenAnt bounty, marketplace, and on-chain collaboration workflows that need CLI guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run a mutable remote CLI through npx @latest.

Mitigation: Prefer a pinned, reviewed CLI version or trusted local install before login, wallet, funding, verification, or messaging workflows.

Risk: The documented commands can perform financial, account-changing, and messaging actions.

Mitigation: Require explicit user confirmation before executing commands that authenticate, fund tasks, verify submissions, send messages, or otherwise change account state.

## Reference(s):

- [OpenAnt ClawHub Skill Page](https://clawhub.ai/ant-1984/skills/openant)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Machine-readable CLI output is requested by appending --json where supported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
