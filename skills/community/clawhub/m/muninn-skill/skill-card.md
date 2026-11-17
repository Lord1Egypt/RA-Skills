## Description:

Production memory for AI agents. Cloudflare-native with 99.1% LOCOMO accuracy. Knowledge graph, temporal reasoning, multi-hop retrieval. Free tier available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phillipneho](https://clawhub.ai/user/phillipneho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Muninn Memory to add persistent semantic, episodic, and procedural memory to AI agents through MCP tools or a cloud API. The skill supports memory storage, recall, session briefings, entity tracking, temporal reasoning, and multi-hop retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a persistent memory system and may retain user-provided information.

Mitigation: Only store information you are comfortable retaining, and choose the local or cloud/API embedding path deliberately before installation.

Risk: Integrity verification can rely on a weak default secret if it is not configured.

Mitigation: Set a strong MUNINN_INTEGRITY_SECRET before using integrity verification.

Risk: Publisher, benchmark, cloud, and license claims may matter for adoption decisions.

Mitigation: Verify the publisher, benchmark results, cloud claims, and applicable license before production rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phillipneho/skills/muninn-skill)
- [Muninn cloud dashboard](https://muninn.au/dashboard)
- [LOCOMO benchmark repository](https://github.com/snap-research/locomo)
- [Artifact README](README.md)
- [LOCOMO analysis](docs/LOCOMO_ANALYSIS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API examples, and MCP memory-tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Node for local use, Ollama for local embeddings, MUNINN_API_KEY for cloud mode, and MUNINN_INTEGRITY_SECRET when integrity verification is enabled.]

## Skill Version(s):

2.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
