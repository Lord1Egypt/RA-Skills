## Description: <br>
OpenClaw Bootstrap provides a one-command setup for new OpenClaw installations, including workspace files, learning logs, hooks, scheduled reviews, and community skill setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DjangoZH](https://clawhub.ai/user/DjangoZH) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize or replicate an OpenClaw workspace with standard memory files, learning logs, hooks, scheduled reviews, and community skill setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent automation and memory collection with weak user-facing consent controls. <br>
Mitigation: Install only when long-term local memory, hooks, and scheduled jobs are desired; inspect each file before running the bootstrap and confirm how to disable automation and delete stored memory. <br>
Risk: The bootstrap may perform networked installs for the ClawHub CLI and a community self-improving-agent skill. <br>
Mitigation: Review the install commands first, skip or remove networked installs that are not needed, and run ClawHub login or installation steps manually when appropriate. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with bash commands and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bootstrap is intended to be idempotent and writes local OpenClaw workspace, hook, cron, and learning-log files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
