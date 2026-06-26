## Description: <br>
Parallel autonomous ML research agents with a Director, git worktrees for per-agent experiment branches, a Skills library for validated technique reuse, a Synthesizer that distills collective knowledge overnight, and circadian rhythm for paper reading and creative thinking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuberwastaken](https://clawhub.ai/user/kuberwastaken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML researchers use Litmus to run autonomous OpenClaw subagents that prepare GPU-backed experiment worktrees, execute overnight ML research loops, track results, steer agents, and summarize findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Litmus creates persistent scheduled autonomous agents with broad local tool authority. <br>
Mitigation: Install it only on a dedicated GPU machine where overnight autonomous execution, cron jobs, and local repository mutation are acceptable; review scheduled jobs before enabling them. <br>
Risk: Optional ClawRxiv publishing can send research content outside the local environment. <br>
Mitigation: Keep ClawRxiv disabled unless external posting is intended, restrict the API key to that service, and review what agents publish. <br>
Risk: Runtime state, experiment worktrees, and configuration are written under ~/.litmus/. <br>
Mitigation: Know how to stop agents, remove scheduled jobs, and delete ~/.litmus/ before deployment; avoid storing valuable API keys in plaintext configuration. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kuberwastaken/litmus) <br>
- [README](README.md) <br>
- [Installation guide](INSTALL.md) <br>
- [Onboarding guide](references/onboarding.md) <br>
- [Worker agent loop](references/program.md) <br>
- [Director workflow](references/director.md) <br>
- [Leisure workflow](references/leisure.md) <br>
- [Dawn workflow](references/dawn.md) <br>
- [Watchdog workflow](references/watchdog.md) <br>
- [Digest workflow](references/digest.md) <br>
- [ClawRxiv integration](references/clawrxiv.md) <br>
- [Default configuration](configs/default.json) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch) <br>
- [Litmus documentation](https://litmus.kuber.studio/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, configuration paths, agent prompts, and JSON result records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Linux or macOS machines with an NVIDIA CUDA GPU; writes runtime state under ~/.litmus/.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
