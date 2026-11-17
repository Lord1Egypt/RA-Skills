## Description:

Provides persistent local memory for Hermes, OpenClaw, and other agents, including automatic capture, cross-session retrieval, governance rules, maintenance jobs, dashboard review, and pgvector search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunme1977](https://clawhub.ai/user/sunme1977)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to let an agent capture important facts, preferences, decisions, and project context across sessions while keeping retrieval and review tied to a local Sidecar deployment. It is intended for self-hosted agent memory workflows that need semantic search, backup commands, maintenance jobs, and governance-aware behavior rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent cross-session memory capture can retain identity, preferences, project details, infrastructure settings, and session content longer than expected.

Mitigation: Review retained memories regularly, delete entries that should not persist, and treat the local memory database as sensitive data.

Risk: Automatic background jobs can continue capturing or processing memory after installation.

Mitigation: Disable or delete any cron jobs that are not needed, especially reminder or maintenance jobs that retain or summarize user data.

Risk: The skill depends on local Sidecar connectivity and API-key based access.

Mitigation: Confirm the Sidecar URL remains local and use a dedicated low-privilege API key.

Risk: Remote setup scripts and global governance hooks can affect agent behavior and local tooling.

Mitigation: Review the remote project and setup scripts before installation, and scan the skill before deployment.

## Reference(s):

- [Enforce Governance Architecture](references/enforce-architecture.md)
- [ClawHub release page](https://clawhub.ai/sunme1977/skills/hermesclawzero-auto-memory)
- [GitHub project link from artifact](https://github.com/SunMe1977/HermesClawZero-ConfigSidecar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands, configuration snippets, and agent behavior guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory capture, search, backup, setup, and governance guidance for an agent; no structured multi-dimensional output.]

## Skill Version(s):

3.0.2 (source: server release metadata; artifact frontmatter and changelog show 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
