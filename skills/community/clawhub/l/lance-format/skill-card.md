## Description:

Deep reference for Lance v15 columnar format, its Rust crates, and pylance - file encodings, table format, indexes, schema evolution, time travel. Use when building on the Lance crates or reading .lance datasets, not the LanceDB product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers working with Lance crates or pylance use this reference to understand file and table formats, indexes, schema evolution, version compatibility, and time travel. It does not cover the LanceDB product API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples that write or delete data could affect a live Lance dataset if copied directly.

Mitigation: Use a fresh dataset path and credentials limited to the intended dataset.

Risk: Remote storage examples can expose credentials or use insecure transport when adapted carelessly.

Mitigation: Use HTTPS and credentials scoped to the intended dataset.

Risk: Cleanup and retention changes can make older data unavailable.

Mitigation: Preserve required retention protections and immutable backups; use a suitable separate bucket rather than blindly disabling Object Lock.

Risk: External dependencies and upstream provenance are unverified in the release evidence.

Mitigation: Check relevant upstream documentation and dependencies before relying on version-sensitive guidance.

## Reference(s):

- [Publisher homepage and skill source page](https://github.com/tenequm/skills/tree/main/skills/lance-format)
- [Lance documentation](https://lance.org)
- [Lance Java API documentation](https://www.javadoc.io/doc/org.lance/lance-core/latest/index.html)
- [Lance Python package index](https://pypi.fury.io/lance-format)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Topic-specific reference answers with version and compatibility details.]

## Skill Version(s):

0.22.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
