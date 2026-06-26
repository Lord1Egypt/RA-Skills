## Description: <br>
Automatically analyze and reduce OpenClaw token waste through context compression, tool-call deduplication insights, model selection guidance, and session hygiene checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkhaytman87](https://clawhub.ai/user/mkhaytman87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect OpenClaw session token usage, plan compression, check session health, and estimate token needs before expensive task batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads OpenClaw session metadata and transcript snippets while analyzing or compressing sessions. <br>
Mitigation: Run it only in workspaces where the operator is allowed to inspect those sessions, and review generated reports or compression files before sharing them. <br>
Risk: The `--cleanup --apply` mode can restart the OpenClaw gateway when stuck sessions are detected. <br>
Mitigation: Use plan-only `--cleanup` first and run `--cleanup --apply` only when a gateway restart is acceptable. <br>
Risk: The packaged command may depend on a `token-optimize` wrapper that is not present in the artifact file list. <br>
Mitigation: Verify the command wrapper or invoke the Python CLI directly before relying on the packaged command path. <br>


## Reference(s): <br>
- [Token Optimizer ClawHub page](https://clawhub.ai/mkhaytman87/mkhaytman-token-optimizer) <br>
- [Token Optimizer Operating Notes](references/operating-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text reports, optional JSON reports, Markdown compression snapshots, and configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write reports and compressed summaries under the OpenClaw workspace token-usage directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
