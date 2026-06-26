## Description: <br>
Organizes agent memory into a scalable hybrid structure with a lean MEMORY.md routing table, topic and contact files, and optional daily, weekly, monthly, and yearly distillation layers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richgoodson](https://clawhub.ai/user/richgoodson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up and maintain durable, organized agent memory across active projects, contacts, and long-running time horizons while keeping MEMORY.md concise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains persistent workspace memory files that may be loaded into future agent context. <br>
Mitigation: Review setup and migration plans before approving changes, and do not store secrets, API keys, passwords, or sensitive personal data in MEMORY.md or linked memory files. <br>
Risk: Migration or setup could change existing memory organization. <br>
Mitigation: Require explicit approval before creating, deleting, or refactoring memory files, and preserve existing daily, weekly, monthly, and yearly archives during upgrades. <br>
Risk: Optional time-based distillation can overlap with memory-wiki syntheses when both are enabled. <br>
Mitigation: Prefer the standard preset or disable time_layers when memory-wiki is enabled unless chronological archives are intentionally needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/richgoodson/hierarchical-agent-memory) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Onboarding Guide](references/onboarding-guide.md) <br>
- [Migration Guide: v2.x to v3.0](references/migration-v2-to-v3.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose workspace memory file and configuration changes; user approval is required before modifying existing memory files.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
