## Description: <br>
Helps agents configure, validate, operate, and troubleshoot Hookaido webhook ingress, durable queues, delivery modes, signature verification, retry policy, and dead-letter queue workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[7schmiede](https://clawhub.ai/user/7schmiede) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to implement Hookaido webhook endpoints, configure authenticated pull or push delivery, validate runtime configuration, inspect queue health, and triage backlog or dead-letter queue incidents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide production webhook queue mutations, DLQ deletes, runtime control, exec-based handlers, and live webhook delivery actions. <br>
Mitigation: Use read-only diagnostics by default and require explicit operator approval before production mutations, DLQ deletes, runtime control, exec delivery changes, or sending real webhook payloads to live services. <br>
Risk: Webhook operation requires sensitive tokens and ingress secrets. <br>
Mitigation: Keep secrets in environment variables or file references, validate configuration before runtime use, and avoid disabling authentication for tests or troubleshooting. <br>
Risk: Downloaded Hookaido release binaries introduce supply-chain risk. <br>
Mitigation: Use pinned Hookaido v2.6.0 install sources and verify release artifact SHA256 checksums before installation. <br>


## Reference(s): <br>
- [Hookaido Operations Reference](references/operations.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/7schmiede/hookaido) <br>
- [Public Skill Repository](https://github.com/7schmiede/claw-skill-hookaido) <br>
- [Upstream Hookaido Project](https://github.com/nuetzliches/hookaido) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, HCL configuration snippets, JSON examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for installing Hookaido, validating Hookaidofile configuration, running local services, configuring MCP mode, and calling webhook queue APIs.] <br>

## Skill Version(s): <br>
2.6.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
