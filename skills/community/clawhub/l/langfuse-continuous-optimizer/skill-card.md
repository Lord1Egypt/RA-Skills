## Description: <br>
Continuous LangFuse-driven optimization loop for OpenClaw/OpenRouter model routing and prompt usage controls with persistent local memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ekalb81](https://clawhub.ai/user/ekalb81) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Clawfuse to ingest LangFuse observations and evaluator scores, generate task-level routing policy JSON, and run safe scheduled promotion cycles for OpenClaw/OpenRouter model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LangFuse credentials and local telemetry snapshots may expose sensitive project data. <br>
Mitigation: Prefer environment variables over persisted secrets, avoid --persist-secrets unless necessary, and keep the optimizer output directory private. <br>
Risk: Promoting a generated routing policy can change live model routing behavior. <br>
Mitigation: Review staged routing_policy.json output first, run non-destructive cycles by default, and enable --promote-live-policy only after validating quality, cost, and latency constraints. <br>
Risk: Daemon mode can repeatedly update policies from recent telemetry before operational practices are validated. <br>
Mitigation: Avoid daemon mode on production routing until generated policies, rollback expectations, and data retention practices have been reviewed. <br>


## Reference(s): <br>
- [Clawfuse on ClawHub](https://clawhub.ai/ekalb81/langfuse-continuous-optimizer) <br>
- [Closed-Loop Playbook](references/closed-loop-playbook.md) <br>
- [Data Contracts](references/data-contracts.md) <br>
- [LangFuse API Overview](https://langfuse.com/docs/api-and-data-platform/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON and CSV policy artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce staged routing_policy.json files, model_stats.csv summaries, persisted configuration, raw LangFuse snapshots, and optimizer memory under configured local paths.] <br>

## Skill Version(s): <br>
0.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
