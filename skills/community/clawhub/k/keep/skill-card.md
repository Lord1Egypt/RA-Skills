## Description:

Reflective Memory gives agents persistent semantic memory, reflective prompts, and CLI or MCP workflows for storing, searching, and updating notes, files, URLs, and working intentions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hughpyle](https://clawhub.ai/user/hughpyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give agents persistent memory across sessions, retrieve relevant prior context, maintain current intentions, and capture learnings or commitments during work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation content and other agent context across sessions.

Mitigation: Review stored memory regularly, remove sensitive entries when needed, and consider disk encryption or local-only providers for sensitive deployments.

Risk: The skill can index broad workspace file trees and watch files for changes.

Mitigation: Narrow configured index paths and add exclusions for secrets, credentials, logs, and other sensitive files before enabling watches.

Risk: First-time setup may modify workspace-local agent configuration and install hooks or integrations.

Mitigation: Review generated configuration before relying on it, use KEEP_NO_SETUP=1 when automatic setup is not desired, and document how to remove hooks, watches, and stored memory.

Risk: Remote model providers or the hosted service may receive content for summarization, embeddings, or shared memory if configured.

Mitigation: Prefer local providers for sensitive content or explicitly approve API and hosted-service configuration before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hughpyle/skills/keep)
- [Quick Start](docs/QUICKSTART.md)
- [Agent Reference Card](docs/REFERENCE.md)
- [MCP Integration](docs/KEEP-MCP.md)
- [OpenClaw Integration](docs/OPENCLAW-INTEGRATION.md)
- [Python API Reference](docs/PYTHON-API.md)
- [PyPI Package](https://pypi.org/project/keep-skill/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, CLI text, JSON, and YAML-frontmatter outputs depending on interface and flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tools expose memory flows, prompt rendering, and help topics; CLI commands can emit summaries, IDs, full YAML-frontmatter records, or JSON.]

## Skill Version(s):

0.109.0 (source: SKILL.md frontmatter, pyproject.toml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
