## Description:

A generic memory-management skill for hybrid retrieval, automatic memory extraction, session-based consolidation, and PluginEval quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donmeusi](https://clawhub.ai/user/donmeusi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Metaclaw to search local memory with semantic, keyword, or hybrid retrieval, extract preferences and project facts from sessions, and maintain skill quality with PluginEval checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local memory and session content and persist extracted preferences or project facts.

Mitigation: Install only where that local memory access is intended, set the workspace deliberately, and review extracted content before relying on it.

Risk: Scheduled memory processing can repeatedly process or consolidate local memory without an interactive review step.

Mitigation: Run digest and extraction commands in dry-run mode first and enable cron only after outputs and retention behavior have been reviewed.

Risk: Auto-fix functionality can mutate skill files when write mode is enabled.

Mitigation: Treat --allow-write as an administrative maintenance mode and review diffs after any auto-fix run.

Risk: The security scan reports a local file-access boundary bug.

Mitigation: Use an isolated or intended workspace, avoid untrusted date inputs, and keep dependency versions pinned where possible.

## Reference(s):

- [Metaclaw ClawHub release](https://clawhub.ai/donmeusi/skills/metaclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands; scripts can emit JSON results and update Markdown memory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local memory/session files, persist extracted memory content, and modify skill files only when explicit write modes are used.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact changelog, released 2026-04-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
