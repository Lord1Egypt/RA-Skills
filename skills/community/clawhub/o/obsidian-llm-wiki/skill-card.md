## Description:

A personal Obsidian knowledge-base workflow that helps agents ingest source material, maintain linked Markdown wiki pages, run vault health checks, and produce synthesis pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddiewang-zhhx](https://clawhub.ai/user/eddiewang-zhhx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to initialize and maintain an Obsidian vault as a structured Markdown wiki from web pages, videos, PDFs, local files, and pasted text. It supports ingest, query, digest, status, and lint workflows for a personal knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The initializer and workflows can create or overwrite local Obsidian vault files.

Mitigation: Run the initializer only on a new or backed-up vault, and review affected files before using it on an existing non-empty vault.

Risk: The skill may run local commands and third-party extraction tools for URLs, videos, PDFs, and other source material.

Mitigation: Install extractors in an isolated environment with pinned versions, and review commands before execution.

Risk: Material extraction can fetch content from network URLs supplied by the user.

Mitigation: Use trusted source URLs and avoid sending sensitive or private content to unreviewed extraction tools.

Risk: Using Obsidian CLI content arguments for long Markdown can truncate generated wiki pages.

Mitigation: Use direct file writes for long content and verify generated pages after writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eddiewang-zhhx/skills/obsidian-llm-wiki)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated Obsidian Markdown files and templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local vault files such as raw materials, wiki pages, indexes, logs, and templates.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
