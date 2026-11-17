## Description:

Nima Core provides persistent memory, emotional intelligence, semantic recall, memory pruning, affect analysis, and embedding options for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dmdorta1111](https://clawhub.ai/user/dmdorta1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw can add persistent conversation memory, semantic recall, affect tracking, and memory maintenance to agents. The skill is suited for local-first agent memory workflows with optional remote embedding providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain sensitive chats, thinking-like content, affect state, and recalled context across sessions.

Mitigation: Treat the local memory store as sensitive data, restrict filesystem access, and review retention and pruning settings before deployment.

Risk: Remote embedding providers can receive text content when Voyage or OpenAI embedding modes are configured.

Mitigation: Use local embeddings unless remote processing is explicitly approved, and configure API keys only for approved providers.

Risk: Installer, upgrade, doctor, and cron workflows can make local changes or run against mutable local configuration.

Mitigation: Review scripts before execution, pin trusted release artifacts, avoid untrusted .env files, and review or disable precognitive cron jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dmdorta1111/skills/nima-core)
- [README](README.md)
- [Installation guide](INSTALL.md)
- [Security policy](SECURITY.md)
- [Changelog](CHANGELOG.md)
- [Quickstart](QUICKSTART.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets; runtime hooks provide recalled context and affect hints as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores memories locally by default and may use remote embedding APIs when configured.]

## Skill Version(s):

3.1.5 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
