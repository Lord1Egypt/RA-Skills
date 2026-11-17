## Description:

Request expert help by submitting queries to the HeySummon platform, which routes them to registered human providers for assistance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomasansems](https://clawhub.ai/user/thomasansems)

### License/Terms of Use:


## Use Case:

Developers and AI-agent operators use Hey Summon when an agent is blocked and needs to route a help request to a registered human expert through the HeySummon platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a persistent background watcher and use a local OpenClaw gateway token.

Mitigation: Review before installing, run only with a trusted HeySummon endpoint, prefer HTTPS for non-local servers, and treat the OpenClaw gateway token as sensitive.

Risk: Auto-sync behavior can accidentally publish local secrets or request state.

Mitigation: Do not run auto-sync.sh until a restrictive .gitignore and staging allowlist are in place.

Risk: Local files such as .env, providers.json, .keys, .requests, and watcher logs may contain credentials or sensitive conversation context.

Mitigation: Keep these files out of commits and backups unless explicitly intended, avoid sending secrets or sensitive context, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thomasansems/skills/heysummon)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, provider registry, key, request-tracking, log, and notification files during use.]

## Skill Version(s):

0.1.0-beta (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
