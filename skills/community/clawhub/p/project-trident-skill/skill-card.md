## Description:

Give your AI agent genuine continuity, identity, and resilience across every session and deployment with a four-tier persistent memory stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shivaclaw](https://clawhub.ai/user/shivaclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Project Trident to add durable, hierarchical memory, signal routing, migration support, and backup guidance to OpenClaw agents. It is intended for agents that need continuity across sessions, deployments, crashes, and updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain broad long-term memory about conversations, identity, preferences, projects, and decisions.

Mitigation: Install only when persistent agent memory is intended, keep initial setup local-only, and review what memory categories are stored before enabling automated routing.

Risk: Optional cloud or vector indexing can expose sensitive memory if used without controls.

Mitigation: Avoid optional cloud or vector indexing until an allowlist, secret redaction process, and access controls are in place.

Risk: Automated backups can commit sensitive memory without review.

Mitigation: Replace unattended git add -A backups with reviewed commits or encrypted backups to a private repository.

Risk: Setup guidance may include unpinned binary downloads or curl-to-shell style commands.

Mitigation: Verify installers, binaries, and hashes independently before executing installation commands.

## Reference(s):

- [Trident Lite: Memory Without Docker](references/trident-lite.md)
- [Trident Deployment Guide](references/deployment-guide.md)
- [Platform Guide: Windows, Mac, and Linux](references/platform-guide.md)
- [Trident Cost Calculator](references/cost-calculator.md)
- [Cost Tuning for Trident Memory](references/cost-tuning.md)
- [Project Trident repository](https://github.com/ShivaClaw/project-trident)
- [Project Trident issue tracker](https://github.com/ShivaClaw/project-trident/issues)
- [Shiva memory homepage](https://github.com/ShivaClaw/shiva-memory)
- [ClawHub skill page](https://clawhub.ai/shivaclaw/skills/project-trident-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and PowerShell command blocks plus included shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or migrate local memory files, cron prompts, audit logs, and backups when users run the included scripts.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
