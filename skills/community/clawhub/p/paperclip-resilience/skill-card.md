## Description: <br>
Production resilience patterns for Paperclip AI agent orchestration, including spawn fallback, model rotation, run recovery, blocker routing, and task injection for OpenClaw and Paperclip deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levineam](https://clawhub.ai/user/levineam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers operating Paperclip agents through OpenClaw use this skill to recover failed runs, retry provider failures with fallback models, route blocked sessions, and enrich spawned tasks with issue or pull request context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically send task and session data to Paperclip APIs and configured webhooks. <br>
Mitigation: Use only trusted Paperclip instances and webhook endpoints, avoid placing secrets or sensitive business context in tasks, and review configuration before enabling automated routing. <br>
Risk: Automated recovery and fallback behavior can re-run agents or duplicate work if retry controls are too broad. <br>
Mitigation: Configure explicit approvals, retry limits, dry-run checks, logging, and redaction before unattended scheduling. <br>
Risk: Task-file and task-payload handling can expose local data if operators point the skill at sensitive files. <br>
Mitigation: Use the documented validation boundaries, keep task payloads scoped, and review any @file inputs before execution in workspaces with private code or customer data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/levineam/paperclip-resilience) <br>
- [Architecture documentation](docs/architecture.md) <br>
- [Security audit report](SECURITY-AUDIT-REPORT.md) <br>
- [Configuration schema](config.schema.json) <br>
- [Paperclip](https://github.com/paperclipai/paperclip) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Paperclip issue 276: auto-requeue agent on failure](https://github.com/paperclipai/paperclip/issues/276) <br>
- [Paperclip issue 1845: crash recovery wakeup](https://github.com/paperclipai/paperclip/issues/1845) <br>
- [Paperclip issue 1861: model fallback after 429](https://github.com/paperclipai/paperclip/issues/1861) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets, shell commands, JSON configuration, and generated task text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single operator-facing stream; configured commands may interact with local OpenClaw state, Paperclip APIs, and configured webhook destinations.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
