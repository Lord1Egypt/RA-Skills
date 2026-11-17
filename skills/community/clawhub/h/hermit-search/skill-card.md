## Description:

Local semantic search over knowledge base collections powered by Hermit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxxgqcoder](https://clawhub.ai/user/xxxgqcoder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base users use this skill to install Hermit, manage local collections, index folders, and query documents with semantic search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path runs mutable third-party code and downloads unverified model assets.

Mitigation: Install only from a trusted Hermit source, prefer a pinned commit or signed release, and verify model sources where possible.

Risk: Indexing broad local folders can expose credentials, private keys, tokens, browser profiles, or unrelated sensitive files.

Mitigation: Index only specific intended folders and configure ignore rules before adding a collection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxxgqcoder/skills/hermit-search)
- [Hermit homepage](https://github.com/xxxgqcoder/hermit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hermit CLI commands return JSON, with optional pretty formatting.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
