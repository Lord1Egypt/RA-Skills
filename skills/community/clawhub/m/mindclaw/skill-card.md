## Description:

MindClaw provides persistent memory and a knowledge graph for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blue8x](https://clawhub.ai/user/blue8x)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use MindClaw to give AI agents structured long-term memory, searchable recall, context blocks, and OpenClaw Markdown synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can store and retrieve broad long-term memory, including content later injected into prompts.

Mitigation: Use a dedicated database and agent namespace, and avoid storing secrets, regulated data, or sensitive personal information.

Risk: Setup, import, capture, sync, and hard-delete actions can mutate configuration, memory stores, or Markdown memory files.

Mitigation: Require explicit user approval for those tools and back up memory files before sync or import.

Risk: Semantic search can depend on trusted local services such as Ollama.

Mitigation: Run local embedding services only in trusted environments and review their configuration before enabling semantic recall.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blue8x/skills/mindclaw)
- [README](README.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, XML, and JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include retrieved memories, generated context blocks, memory mutation results, setup results, sync results, and import or export summaries.]

## Skill Version(s):

0.3.1 (source: release metadata, pyproject.toml, clawhub.yaml, CHANGELOG, src/mindclaw/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
