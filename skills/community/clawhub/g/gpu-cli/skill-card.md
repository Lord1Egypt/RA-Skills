## Description:

Safely runs local gpu commands through a guarded wrapper with preflight checks, dry-run behavior, budget caps, and runtime caps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angusbezzina](https://clawhub.ai/user/angusbezzina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect GPU CLI state, run remote GPU workloads, and start ML training or inference tasks through a guarded command wrapper. It is intended for local agent workflows where the user already has GPU CLI and provider credentials configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags broader Bash permission than the documented runner-only boundary.

Mitigation: Review before installing and prefer a release where the publisher narrows Bash permission to the bundled runner.

Risk: The security guidance flags pipe-to-shell install advice as unsafe.

Mitigation: Do not run the suggested curl-to-shell installer without independent verification; install gpu through a trusted channel.

Risk: GPU commands may use the user's configured provider account and incur costs.

Mitigation: Keep dry-run and confirmation enabled, and retain price and runtime caps before starting paid GPU resources.

## Reference(s):

- [GPU CLI Documentation](https://gpu-cli.sh/docs/ai-agent-skill)
- [GPU CLI Homepage](https://gpu-cli.sh)
- [GPU CLI Repository](https://github.com/gpu-cli/gpu)
- [ClawHub Skill Page](https://clawhub.ai/angusbezzina/skills/gpu-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON-capable command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream GPU CLI command results; JSON output is recommended for structured status, inventory, logs, and configuration responses.]

## Skill Version(s):

1.2.0 (source: server release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
