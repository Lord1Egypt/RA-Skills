## Description:

Neural Memory CN provides a neural network-inspired memory system with activation spreading and associative retrieval that works locally by default and can use a configured LLM for intent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunlight-bulling](https://clawhub.ai/user/sunlight-bulling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add a local neural-memory module for learning, associative retrieval, activation-spreading queries, and optional LLM-assisted intent analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive memory, profile, or query-derived data.

Mitigation: Use a dedicated storage path with restrictive file permissions and avoid storing private or business-sensitive content unless that use is intended.

Risk: Optional LLM or embedding features may send memory or query text to the configured provider.

Mitigation: Keep LLM and embedding features disabled unless the provider and data flow are approved for the intended data.

Risk: API keys may be exposed if passed through command-line arguments or stored carelessly.

Mitigation: Prefer environment variables or a secret manager for credentials and avoid putting API keys in shell history or shared configuration files.

## Reference(s):

- [Neural Memory CN ClawHub Skill Page](https://clawhub.ai/sunlight-bulling/skills/neural-memory-cn)
- [API Reference](references/api.md)
- [Architecture](references/architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, YAML, and JSON snippets; Python APIs return dictionaries and lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create and update local JSON memory, synapse, embedding, and activation-log files; optional LLM and embedding features may use configured external providers.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
