## Description:

Openclaw Soul deploys an OpenClaw self-evolution framework with workspace constitution files, evolving identity templates, heartbeat setup, memory architecture, goal tracking, optional dependency skills, and guided personality bootstrapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kianzzz](https://clawhub.ai/user/kianzzz)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent developers use this skill to initialize a persistent agent workspace, define the agent's identity and operating rules, configure memory and heartbeat behavior, and install optional self-improvement and governance modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs durable automation such as heartbeat, memory, and auto-commit scheduled jobs.

Mitigation: Review scheduled jobs before enabling the skill, remove unwanted cron entries, and keep deployment supervised until the workspace behavior is understood.

Risk: Persistent prompt control and memory profiling can shape future agent sessions and store conversation-derived information.

Mitigation: Review generated identity, constitution, memory, and governance files before use; prefer supervised or advisory governance for identity and rule changes.

Risk: Optional memory optimization scripts are flagged by security guidance for unsafe shell-command paths.

Mitigation: Avoid those optional scripts until command construction is fixed and reviewed.

Risk: Remote embeddings, social-feed ingestion, and API key handling can expose sensitive data or credentials if enabled carelessly.

Mitigation: Enable only trusted providers and sources, keep secrets in intended environment variables or secret stores, and avoid pasting API keys into chat or shell profiles unless that persistence is deliberate.

## Reference(s):

- [Openclaw Soul ClawHub Page](https://clawhub.ai/kianzzz/skills/openclaw-soul)
- [README](README.md)
- [Bootstrap Guide](references/bootstrap-guide.md)
- [Memory Architecture Template](references/memory-architecture-template.md)
- [Dynamic Personality Add-on](references/dynamic-personality-addon.md)
- [User Observation Hook](references/hooks/user-observation/HOOK.md)
- [EvoClaw Schema](fallback/evoclaw/references/schema.md)
- [EvoClaw External Sources](fallback/evoclaw/references/sources.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands, JSON configuration, and copied template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent workspace files, memory directories, scheduled-job configuration, and optional dependency skill setup.]

## Skill Version(s):

3.0.1 (source: server release metadata, released 2026-04-02; artifact metadata reports 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
