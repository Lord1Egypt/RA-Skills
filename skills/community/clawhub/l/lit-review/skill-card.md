## Description:

Conduct structured literature reviews with systematic search and synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to collect academic papers for a topic, filter and cluster results, and generate structured literature-review drafts with references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics are sent to external academic APIs.

Mitigation: Avoid confidential or unpublished research topics unless the execution environment permits those disclosures.

Risk: The artifact uses a plaintext arXiv API endpoint.

Mitigation: Prefer HTTPS or route requests through approved egress controls before production use.

Risk: Optional LLM writing can send prompts and a user-provided API key to a configurable endpoint.

Mitigation: Enable LLM writing only with a trusted HTTPS endpoint, protect the API key, and allowlist the provider.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/paudyyin/skills/lit-review)
- [README](artifact/README.md)
- [Skill documentation](artifact/skill.md)
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search)
- [arXiv API](http://export.arxiv.org/api/query)
- [CrossRef Works API](https://api.crossref.org/works)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown literature-review draft with references; optional bibliography file when using the included command-line entry point]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on results returned by external academic APIs and, when enabled, a configured LLM endpoint.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
