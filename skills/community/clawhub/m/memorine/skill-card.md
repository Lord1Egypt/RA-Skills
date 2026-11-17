## Description:

Human-like memory for AI agents. Facts, events, procedures, contradiction detection, forgetting curve, and cross-agent sharing. Pure Python + SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[osvfelices](https://clawhub.ai/user/osvfelices)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Memorine to add persistent local memory to OpenClaw or MCP-compatible agents, including facts, event history, procedure outcomes, contradiction handling, and shared team knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists agent memories and can share knowledge across agents.

Mitigation: Install only where persistent memory is appropriate, control database paths, file permissions, backups, and sharing rules, and avoid storing secrets or regulated data unless those controls are in place.

Risk: The release installs Python package code to run an MCP server.

Mitigation: Pin the memorine package version and hash for production use and review package updates before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/osvfelices/skills/memorine)
- [Project Homepage](https://github.com/osvfelices/memorine)
- [PyPI Package](https://pypi.org/project/memorine/)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, Python, and bash examples; MCP tool responses are text or JSON-compatible data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and recalls local SQLite-backed agent memory; optional extras add semantic search and a terminal dashboard.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
