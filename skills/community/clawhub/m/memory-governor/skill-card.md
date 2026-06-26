## Description: <br>
Memory governance kernel for AI agents that complements the OpenClaw 2026.6.x memory stack (Dreaming, Active Memory, Memory Wiki, People Wiki, Skill Workshop / Workboard) with explicit correction staging, target-class routing, compiled-surface boundaries, scope/privacy rules, and safer manual hardening rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sakenw](https://clawhub.ai/user/sakenw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to govern agent memory capture, routing, promotion, exclusion, adapter boundaries, and scoped-memory handling in hosts with multiple memory layers or memory-writing skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory-routing rules may cause sensitive or short-lived information to be stored in local memory paths if the host maps targets too broadly. <br>
Mitigation: Decide permitted adapter paths before integration, exclude secrets and sensitive personal data, and require scoped entries for project, chat, or agent-specific memory. <br>
Risk: Temporary state can become permanent if working buffers, proactive state, imported insights, or learning candidates are promoted without review. <br>
Mitigation: Use the retention guidance, candidate review flow, and host checker before hardening content into durable memory, reusable lessons, system rules, or tool rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sakenw/memory-governor) <br>
- [Publisher profile](https://clawhub.ai/user/sakenw) <br>
- [Memory routing](references/memory-routing.md) <br>
- [Promotion rules](references/promotion-rules.md) <br>
- [Exclusions](references/exclusions.md) <br>
- [Adapters](references/adapters.md) <br>
- [Compiled surfaces](references/compiled-surfaces.md) <br>
- [Installation integration](references/installation-integration.md) <br>
- [Host checker](references/host-checker.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with reference documents, Python helpers, shell scripts, and host configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory-governance decisions and integration artifacts for local host-controlled memory paths.] <br>

## Skill Version(s): <br>
0.3.2 (source: frontmatter, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
