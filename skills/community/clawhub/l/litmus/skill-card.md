## Description:

Litmus turns an OpenClaw instance on a GPU machine into a parallel autonomous ML research lab with worker subagents, git-backed experiments, scheduled direction, synthesis, and morning digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuberwastaken](https://clawhub.ai/user/kuberwastaken)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML researchers use Litmus to set up, run, steer, and monitor autonomous OpenClaw agents that explore machine learning experiments overnight on a dedicated GPU machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-running autonomous research agents and persistent cron jobs can continue consuming local compute after setup.

Mitigation: Install only on a dedicated GPU machine, review setup and cron scripts before use, and confirm you can list, remove, and stop all litmus jobs and worker sessions.

Risk: Setup downloads and runs an upstream ML harness and creates local git worktrees and runtime state under ~/.litmus/.

Mitigation: Pin or verify the upstream harness before running setup and review generated worktrees, commits, and attempt records during operation.

Risk: Optional ClawRxiv publishing can send research writeups outside the local machine and stores an API key in local configuration when enabled.

Mitigation: Keep ClawRxiv disabled unless external publication and local key storage are acceptable, and send the key only to clawrxiv.io.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kuberwastaken/skills/litmus)
- [Litmus documentation](https://litmus.kuber.studio/docs)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Karpathy autoresearch harness](https://github.com/karpathy/autoresearch)
- [Onboarding guide](references/onboarding.md)
- [Research agent program](references/program.md)
- [Director agent](references/director.md)
- [Leisure mode agent](references/leisure.md)
- [Dawn agent](references/dawn.md)
- [Watchdog agent](references/watchdog.md)
- [Daily digest agent](references/digest.md)
- [ClawRxiv integration](references/clawrxiv.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, OpenClaw tool call examples, JSON configuration, and generated research notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, git, and python3; supports Linux and macOS; recommends nvidia-smi and an NVIDIA CUDA GPU; uses ~/.litmus/ for runtime state.]

## Skill Version(s):

1.1.1 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
