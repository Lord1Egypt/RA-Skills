## Description:

Local Memory provides semantic memory storage, retrieval, and deletion using ChromaDB with BGE-small-zh embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangmu-git2](https://clawhub.ai/user/liangmu-git2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to store, retrieve, and delete long-term semantic memories in a local ChromaDB database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory may retain private or sensitive text.

Mitigation: Avoid storing secrets or credentials, review stored memory data periodically, and run the skill in an isolated environment when handling sensitive work.

Risk: First-run setup downloads dependencies and model files despite the offline memory-storage goal.

Mitigation: Use pinned dependencies and a verified local model cache before relying on the skill in a production or restricted-network environment.

Risk: Network and supply-chain behavior is under-disclosed relative to the offline claim.

Mitigation: Review the install script before execution and approve the dependency and model sources in advance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangmu-git2/skills/local-memory)
- [Hugging Face mirror endpoint](https://hf-mirror.com)
- [PyTorch CPU wheel index](https://download.pytorch.org/whl/cpu)

## Skill Output:

**Output Type(s):** [JSON, shell commands, configuration]

**Output Format:** [JSON emitted by Python command-line scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores memory text persistently under the skill data directory; setup may download dependencies and model files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
