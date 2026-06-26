## Description: <br>
Lobster is a workflow runtime for deterministic, typed pipelines with approval gates for agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guwidoe](https://clawhub.ai/user/guwidoe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Lobster to run multi-step automations, monitor pull requests or issues, process typed JSON pipelines, triage email or batch operations, and pause for human approval before side effects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lobster workflows can execute shell commands and invoke external tools, so unreviewed workflows or arguments may cause unintended side effects. <br>
Mitigation: Inspect workflow files and commands before running them, use approval gates before side effects, and avoid untrusted workflow inputs. <br>
Risk: The Clawdbot integration can use CLAWD_URL and CLAWD_TOKEN, and local workflow state may contain sensitive data. <br>
Mitigation: Use least-privilege tokens and clear or relocate ~/.lobster/state/ when it may contain sensitive workflow data. <br>
Risk: The skill depends on an external Lobster CLI or package source. <br>
Mitigation: Install only from a trusted Lobster CLI or package source and review the installed runtime before use. <br>


## Reference(s): <br>
- [ClawHub Lobster skill page](https://clawhub.ai/guwidoe/lobster) <br>
- [Skill-supplied contribution repository](https://github.com/guwidoe/lobster-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool mode may return JSON approval envelopes; workflows can read or write local state under ~/.lobster/state/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
