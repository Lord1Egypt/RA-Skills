## Description:

P2P distributed AI platform for every domain: health, education, science, art, music, agriculture, and law; it helps agents share compute, query specialists, and sync memory with Ed25519 identity, Web of Trust, and end-to-end encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azilbugpinky-ai](https://clawhub.ai/user/azilbugpinky-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use PinkyBrain to turn an OpenClaw agent into a P2P AI node for distributed inference, specialist routing, peer discovery, CRDT memory sync, model sharing, and node administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and update steps rely on mutable external code from the publisher repository.

Mitigation: Use a pinned commit or signed release, review upstream code and dependencies, and avoid applying updates automatically until the source is verified.

Risk: Public mesh, auto-discovery, and model sharing can expose local resources and network metadata.

Mitigation: Keep the node local/private during setup and enable public mesh, auto-discovery, and model sharing only after configuration and trust settings are reviewed.

Risk: Conversation storage and mesh queries may retain or expose sensitive prompts depending on privacy and retention settings.

Mitigation: Avoid sensitive prompts until privacy levels, retention settings, and conversation export behavior are understood and configured.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/azilbugpinky-ai/skills/pinkybrain)
- [Publisher Profile](https://clawhub.ai/user/azilbugpinky-ai)
- [Project Repository](https://github.com/PinkyBrain-ai/pinkybrain)
- [Project Website](https://PinkyBrain-ai.github.io/pinkybrain/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, API endpoint descriptions, and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes a configured PinkyBrain node and may involve local services, peer discovery, mesh participation, model sharing, and update commands.]

## Skill Version(s):

5.3.3 (source: server release evidence; artifact frontmatter reports 5.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
