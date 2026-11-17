## Description:

AI-native GitHub assistant that indexes repositories into Qdrant, supports semantic search across issues, pull requests, code, and repository metadata, and monitors repository activity with Feishu alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ultracold-molecule](https://clawhub.ai/user/ultracold-molecule)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to index GitHub repositories, find related issues and pull requests with natural-language semantic search, inspect recent CI status, and monitor repositories for relevant activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries GitHub through the user's authenticated gh session and can access repository issue, pull request, CI, and metadata content available to that account.

Mitigation: Run it only with an account and repository scope appropriate for the intended task, and review repository targets before indexing or monitoring.

Risk: Indexed issue and pull request text is stored in a local Qdrant collection and sent to local Ollama for embeddings.

Mitigation: Use only approved local storage and model environments for the repositories being indexed, and clear or isolate the Qdrant collection when data should not persist.

Risk: Repository monitoring can forward activity to Feishu through a hard-coded recipient path.

Mitigation: Remove or replace the hard-coded Feishu recipient and require explicit destination review before enabling alert delivery.

Risk: Initializing the index recreates the Qdrant collection and can delete existing local indexed data.

Mitigation: Back up or inspect the existing collection before running init, and avoid init on a live collection unless deletion is intended.

Risk: Subprocess calls compose command strings from repository and argument values.

Mitigation: Validate repository identifiers and use argument-list subprocess calls before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ultracold-molecule/skills/github-semantic)
- [Local Ollama embeddings endpoint used by scripts](http://localhost:11434/api/embeddings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include repository metadata, issue or pull request details, match scores, URLs, labels, timestamps, and optional CI summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
