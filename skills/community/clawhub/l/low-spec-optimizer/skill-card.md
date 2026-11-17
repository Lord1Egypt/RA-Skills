## Description:

Optimize OpenClaw performance on machines with limited resources (4GB RAM or less, old CPUs). Use when (1) user mentions slow performance, high RAM usage, or system lag, (2) running on Raspberry Pi, old laptops, or budget VPS, (3) proactively during heartbeats to check system health, (4) before spawning multiple subagents on low-resource machines. Provides resource monitoring, automatic cleanup, session management, and configuration recommendations for constrained environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lunaviva211-sketch](https://clawhub.ai/user/lunaviva211-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor constrained OpenClaw environments, clean stale local sessions and caches, and choose lighter configuration settings before running heavy agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup helper can delete local session, trash, browser profile, package-cache, and journal data beyond the narrow resource-optimization task.

Mitigation: Run the dry-run mode first, review every target path, and avoid aggressive cleanup unless the user explicitly wants package-cache and journal cleanup.

Risk: Running cleanup with elevated privileges could widen the deletion impact.

Mitigation: Use normal user privileges by default and require explicit user confirmation before any elevated cleanup action.

## Reference(s):

- [Low-Spec Configuration Guide](references/config-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run local shell scripts that report resource usage or clean selected local cache and session paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
