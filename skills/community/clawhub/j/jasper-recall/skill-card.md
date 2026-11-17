## Description:

Local retrieval-augmented memory for AI agents using ChromaDB and sentence-transformers, with shared-memory controls, multi-agent mesh search, and OpenClaw integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emberdesire](https://clawhub.ai/user/emberdesire)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Jasper Recall to index local memory files and session digests, retrieve relevant prior context, and share selected public memories across sandboxed or multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and runtime paths may execute shell commands or setup steps that need review before deployment.

Mitigation: Review and fix shell execution paths before installation, and run setup only in an isolated user account or container until reviewed.

Risk: Unpinned or heavy local dependencies can change behavior or expand the installation footprint.

Mitigation: Pin dependencies, verify package sources, and test the installation in a clean environment before enabling it for regular agent use.

Risk: Private memories can be exposed if the recall server is bound externally or RECALL_ALLOW_PRIVATE is enabled on a shared host.

Mitigation: Keep the recall server bound to localhost, avoid RECALL_ALLOW_PRIVATE on shared systems, and require publicOnly for untrusted or sandboxed agents.

Risk: Existing ChromaDB data may retain old privacy boundaries after fixes or configuration changes.

Mitigation: Rebuild or purge ChromaDB data after privacy-boundary fixes, then re-index only content intended for the target collections.

Risk: Automatic recall can inject irrelevant or sensitive memory into an agent context.

Mitigation: Use publicOnly for sandboxed agents, set a meaningful minScore threshold, and review which collections are searched before enabling autoRecall.

## Reference(s):

- [Jasper Recall ClawHub Listing](https://clawhub.ai/emberdesire/skills/jasper-recall)
- [Jasper Recall GitHub Repository](https://github.com/E-x-O-Entertainment-Studios-Inc/jasper-recall)
- [Jasper Recall npm Package](https://www.npmjs.com/package/jasper-recall)
- [Jasper Recall Product Documentation](https://exohaven.online/products/jasper-recall)
- [Multi-Agent Mesh Documentation](docs/MULTI-AGENT-MESH.md)
- [Shared Memory Specification](docs/SHARED-MEMORY-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command guidance for local memory search, indexing, server use, and plugin configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include retrieved memory snippets, similarity scores, file paths, public-only search results, setup commands, and OpenClaw configuration.]

## Skill Version(s):

0.4.0 (source: ClawHub release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
