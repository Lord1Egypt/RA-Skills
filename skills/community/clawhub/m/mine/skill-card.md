## Description:

Mine Skill launches and manages a Benchmark Subnet worker that uses AWP wallet signing and OpenClaw agents to answer, ask, monitor, and report benchmark activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kilb](https://clawhub.ai/user/kilb)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users can use this skill to run and manage an autonomous Benchmark Subnet worker, including launch, status checks, score review, notifications, logs, and worker shutdown. It is intended for users who understand the wallet-signing and remote benchmark participation model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an autonomous loop that unlocks or signs with an AWP wallet.

Mitigation: Run it only in a dedicated low-privilege environment with a wallet intended for benchmark work.

Risk: Remote benchmark prompts are forwarded to an agent and benchmark content can be sent to configured notification targets.

Mitigation: Use summary or silent notification mode when appropriate and avoid running it where unrelated secrets are present.

Risk: Worker status, logs, and history are written under /tmp and may contain benchmark question and answer content.

Mitigation: Review and clean local worker files after use, especially on shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kilb/skills/mine)
- [Project homepage](https://github.com/awp-core/subnet-benchmark)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands, JSON status/configuration snippets, and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start or manage background worker processes and local files when the user requests worker operations.]

## Skill Version(s):

0.19.2 (source: server release metadata; artifact frontmatter lists 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
