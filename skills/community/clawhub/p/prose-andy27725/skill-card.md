## Description:

OpenProse VM skill pack. Activate on any `prose` command, .prose files, or OpenProse mentions; orchestrates multi-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run, compile, update, and get help for `.prose` programs that orchestrate multi-agent workflows. It supports local files, bundled examples, registry references, and direct URL program references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote `.prose` workflows can be fetched and executed from arbitrary URLs or registry references.

Mitigation: Use only trusted `.prose` programs; inspect and pin remote content before execution.

Risk: The skill can spawn agent sessions and create persistent memory that may outlive a single run.

Mitigation: Keep persistent agents scoped to a project or run unless cross-project memory is intentionally required.

Risk: PostgreSQL state can expose database credentials to spawned sessions or logs.

Mitigation: Use a dedicated least-privilege database, avoid production credentials and `DATABASE_URL`, and do not expose unauthenticated Docker PostgreSQL on shared or reachable hosts.

## Reference(s):

- [OpenProse Homepage](https://www.prose.md)
- [ClawHub Skill Page](https://clawhub.ai/andy27725/skills/prose-andy27725)
- [Publisher Profile](https://clawhub.ai/user/andy27725)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and generated or updated workflow files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute `.prose` workflows, spawn agent sessions, and create runtime state or memory files according to the selected state mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
