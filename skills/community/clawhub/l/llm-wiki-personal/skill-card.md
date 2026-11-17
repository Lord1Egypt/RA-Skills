## Description:

Builds and maintains a local Markdown personal knowledge base from links, files, and pasted text using the llm-wiki methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlalamoon](https://clawhub.ai/user/vlalamoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to initialize, ingest into, query, lint, and visualize a personal wiki that stores extracted source material and generated knowledge pages as local Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and content ingestion can use broad, mutable network behavior through package managers, URL extraction, hosted fallback endpoints, and optional transcript or article tools.

Mitigation: Review commands before execution, install only in trusted environments, prefer local-only extraction where possible, and avoid curl-to-shell installer suggestions unless independently verified.

Risk: Ingested URLs or copied source material may contain private content, token-bearing links, or material the user does not want stored locally as Markdown.

Mitigation: Use the skill only with sources approved for local storage, remove secrets from URLs and pasted text before ingestion, and keep the generated wiki in an access-controlled location.

Risk: Always-download media or browser-based extraction can fetch untrusted remote assets or depend on an authenticated browser session.

Mitigation: Do not enable automatic media downloads for untrusted pages, avoid using authenticated sessions for sensitive accounts, and use manual paste fallback for sources that should not be fetched automatically.

Risk: The package appears incomplete because source-registry TSV files referenced by the scripts are absent from the artifact, which may cause installation or source routing to fail.

Mitigation: Verify the package includes source-registry.tsv and source-record-contract.tsv before release or document manual ingestion fallback until those files are restored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vlalamoon/skills/llm-wiki-personal)
- [Karpathy llm-wiki methodology](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [baoyu-url-to-markdown dependency](https://github.com/JimLiu/baoyu-skills#baoyu-url-to-markdown)
- [wechat-article-to-markdown dependency](https://github.com/jackwener/wechat-article-to-markdown)
- [baoyu-url-to-markdown first-time setup](deps/baoyu-url-to-markdown/references/config/first-time-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files and concise chat guidance with occasional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local wiki folders, source summaries, entity pages, topic pages, indexes, logs, and Mermaid graph snippets.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
