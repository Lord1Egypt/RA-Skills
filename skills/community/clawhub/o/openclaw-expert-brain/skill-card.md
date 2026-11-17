## Description:

Manual interactivo de OpenClaw con 185 fuentes curadas en NotebookLM para responder preguntas sobre instalacion, configuracion, skills, troubleshooting, multi-agent, cron y seguridad en espanol e ingles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[radelqui](https://clawhub.ai/user/radelqui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and architects use this skill to ask OpenClaw setup, configuration, ClawHub, skill, troubleshooting, multi-agent, cron, MCP and security questions against a curated NotebookLM knowledge base. It is useful when an agent needs concise OpenClaw guidance in Spanish or English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions are sent through a third-party nlm/NotebookLM CLI using Google authentication.

Mitigation: Use a reviewed and pinned notebooklm-mcp-cli version in an isolated environment, and do not send credentials, private customer data, or internal secrets.

Risk: The skill depends on local availability of python3 and nlm plus an authenticated NotebookLM session.

Mitigation: Verify python3 and nlm are installed, complete nlm login before use, and configure OPENCLAW_NOTEBOOK_ID when a specific notebook should be queried.

## Reference(s):

- [OpenClaw Expert Brain on ClawHub](https://clawhub.ai/radelqui/skills/openclaw-expert-brain)
- [radelqui publisher profile](https://clawhub.ai/user/radelqui)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-style guidance returned from NotebookLM, sometimes including shell commands or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, nlm, Google authentication, and an OpenClaw NotebookLM notebook ID.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
