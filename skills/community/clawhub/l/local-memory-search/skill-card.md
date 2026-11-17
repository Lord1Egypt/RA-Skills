## Description:

Lightweight semantic search for OpenClaw memory files that builds and queries a local memory index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to search local memory, workspace knowledge, and related Markdown files for relevant snippets with file paths and line numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw memory and knowledge files that may contain private notes, credentials, or sensitive work data.

Mitigation: Review memory contents before indexing and avoid installing or running the skill in workspaces that contain secrets or sensitive information.

Risk: Building the index stores memory-derived content and embeddings in a persistent plaintext file under ~/.openclaw.

Mitigation: Treat the generated index as sensitive data, restrict filesystem access, and delete it when no longer needed.

Risk: The artifact behavior uses a local Ollama embedding component despite documentation describing TF-IDF and no external dependencies.

Mitigation: Confirm Ollama is intended and locally controlled before use, and review the implementation when dependency disclosure matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dagangtj/skills/local-memory-search)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include ranked snippets, source file paths, line ranges, and similarity scores.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
