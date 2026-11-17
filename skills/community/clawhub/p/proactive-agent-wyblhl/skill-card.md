## Description:

Transforms AI agents from task-followers into proactive partners with memory, write-ahead logging, working buffers, compaction recovery, unified search, security hardening, and proactive behavior patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyblhl](https://clawhub.ai/user/wyblhl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add durable local memory, proactive check-ins, write-ahead logging, working buffers, compaction recovery, unified search, and security guardrails to an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to keep durable local memory about a user and their work.

Mitigation: Install only when durable memory is intended, keep memory files out of shared repositories or sync folders unless deliberate, and review or delete memory files regularly.

Risk: Broad conversation capture can store secrets, personal data, or sensitive project details.

Mitigation: Narrow what gets logged, disable full-exchange capture by default, and add redaction for secrets and personal data before using the skill on sensitive projects.

Risk: Helper scripts write local state and memory files when run.

Mitigation: Review the configured memory paths and generated files before deployment, and run the scripts only in workspaces where local state persistence is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wyblhl/skills/proactive-agent-wyblhl)
- [Publisher profile](https://clawhub.ai/user/wyblhl)
- [Proactive Agent Implementation Reference](references/implementation-reference.md)
- [Proactive Tracker](references/proactive-tracker.md)
- [Security Hardening Guide](references/security-hardening.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python helper scripts, JSON status output, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts may write local memory and state files when run.]

## Skill Version(s):

3.1.1 (source: server release metadata; artifact frontmatter reports 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
