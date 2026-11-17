## Description:

Runs Kimi K2.5 and GPT 5.3 Codex in a pre-turn hook and injects their perspectives so an OpenClaw agent can synthesize multiple viewpoints before responding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannydvm](https://clawhub.ai/user/dannydvm)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add on-demand multi-LLM perspective generation to OpenClaw agents before a response is produced. It is intended for workflows where additional viewpoints can help identify missed angles, verification needs, or decision risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent transcript or memory/context content can be sent to configured LLM providers.

Mitigation: Review before installation, prefer local Ollama where appropriate, configure owner/session scoping, and avoid sending sensitive content to external providers.

Risk: Provider-generated text is reintroduced into agent context and can influence responses.

Mitigation: Treat injected perspectives as advisory content, review high-impact outputs, and scan/test the skill before deployment.

Risk: The daemon can run persistently and monitor local agent session files.

Mitigation: Use the daemon only when continuous monitoring is needed, keep file permissions restrictive, and stop or uninstall the service when not in use.

Risk: Security guidance says not to rely on the documented mb keyword trigger unless enforcement is fixed.

Mitigation: Verify trigger behavior in the installed artifact before use and prefer explicit scoping or disabling automatic modes until corrected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dannydvm/skills/openclaw-multi-brain)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)
- [Quick Start](artifact/QUICKSTART.md)
- [Moonshot Chat Completions API](https://api.moonshot.ai/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets; runtime output is injected text perspectives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call configured LLM providers, write local perspective files, and inject generated perspective text into agent context.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json and CHANGELOG.md list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
