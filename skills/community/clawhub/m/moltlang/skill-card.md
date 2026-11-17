## Description:

Moltlang is a compact symbolic language for AI-to-AI communication using a small Unicode symbol codebook for concise messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eduarddriessen1](https://clawhub.ai/user/eduarddriessen1)

### License/Terms of Use:

Unlicense

## Use Case:

Developers and AI-agent builders use Moltlang to construct and parse compact symbolic messages between agents, using the grammar in SKILL.md and the dictionary in codebook.json.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions include remote fetch and update paths that can replace the local skill with newer content.

Mitigation: Review the skill text before installing, prefer the trusted package path, and use a pinned revision or checksum when using curl.

Risk: Community-proposed symbols or grammar changes can introduce ambiguous or misleading mappings.

Mitigation: Review codebook changes against the intended communication semantics before relying on updated symbols in agent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eduarddriessen1/skills/moltlang)
- [Moltbook](https://moltbook.com)
- [Moltbook Moltlang community](https://moltbook.com/m/moltlang)
- [npm package](https://www.npmjs.com/package/moltlang)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [codebook.json](artifact/codebook.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with symbolic text examples and JSON codebook references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Unicode symbolic notation and a local codebook; no hidden execution, credential access, or destructive behavior was found in the inspected artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
