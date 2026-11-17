## Description:

LLM NeverDie helps OpenClaw stay available during model or provider failures by guiding provider-diverse fallback configuration, deploying a standalone Node.js monitor, and optionally sending Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephtandle](https://clawhub.ai/user/josephtandle)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to assess LLM fallback resilience, configure provider-diverse model chains, install a recurring monitor, and receive local or Telegram alerts when model failures are detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can install a recurring background monitor job.

Mitigation: Review the cron entry before enabling it and manually verify that the job is removed when uninstalling.

Risk: Telegram credentials may be stored in a local configuration file or exposed through command history when passed as command arguments.

Mitigation: Prefer file-only mode or environment-based secrets, restrict .neverdie-config.json permissions to the owning user, avoid passing bot tokens on the command line, and rotate any token previously supplied that way.

Risk: Telegram alerts introduce optional outbound network traffic.

Mitigation: Use file-only alerts unless Telegram is required, and configure Telegram only after reviewing the external notification behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephtandle/skills/neverdie)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local OpenClaw monitor, config, state, alert, and cron job files when the user runs the provided setup commands.]

## Skill Version(s):

1.2.0 (source: server evidence release.version and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
