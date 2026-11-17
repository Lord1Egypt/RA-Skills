## Description:

Local-first, multi-agent persistent memory for AI assistants. Use it to install, operate, connect, diagnose, or update Memoria on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nieto42](https://clawhub.ai/user/nieto42)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Memoria to install and run a local-first persistent memory service for AI assistants, connect agents through MCP or OpenClaw, and diagnose recall, capture, sharing, and synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can read and store conversation context for connected agents.

Mitigation: Install only for trusted use cases, keep sensitive workflows local, and disable automatic capture or sharing when persistent memory is not wanted.

Risk: The documented installer uses a curl-to-shell path and can start a background service with login autostart.

Mitigation: Prefer a pinned, inspectable installer or verified release, review the install script before running it, and disable autostart if background persistence is not desired.

Risk: Remote LLM providers and imported or shared memories can expose or influence conversation data.

Mitigation: Use local LLM providers for sensitive content, configure remote providers only with explicit approval, and review imported or shared memories before allowing recall.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nieto42/skills/openclaw-memoria)
- [Memoria project homepage](https://github.com/Primo-Studio/openclaw-memoria)
- [Memoria website](https://primo-studio.fr/app/memoria)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local installation, pairing, diagnostic, update, and risk guidance.]

## Skill Version(s):

3.35.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
