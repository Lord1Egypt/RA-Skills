## Description:

A content rewriting skill for extracting copy, analyzing content structure and style, storing and querying reference examples, and drafting platform-adapted rewrites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pyzxs](https://clawhub.ai/user/pyzxs)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content operators use this skill in OpenClaw to extract source copy, analyze high-performing content patterns, retrieve similar examples, and produce platform-adapted rewrite drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User content may be persisted in a vector store and retrieved later.

Mitigation: Avoid storing confidential drafts, personal data, client content, or copyrighted source material unless the storage location, retention behavior, and deletion process are confirmed.

Risk: Content may be sent to an external embedding service during vectorization.

Mitigation: Use a scoped embedding API key, review the configured embedding endpoint, and avoid submitting sensitive input.

Risk: The documented vector-store installation command does not pin a reviewed tool version.

Mitigation: Install a reviewed pinned version of jl-vector-store in a least-privilege environment before use.

Risk: Generated rewrites may be too close to source content or unsuitable for the target platform.

Mitigation: Review outputs for originality, rights, and target-platform policy compliance before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pyzxs/skills/hit-content-rewriter)
- [README.md](README.md)
- [Content analyzer design](references/content-analyzer.md)
- [Design philosophy](references/design-philosophy.md)
- [Rewrite quick reference](references/rewrite-quick-reference.md)
- [Rewrite strategies](references/rewrite_strategies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted copy, analysis reports, storage or query confirmations, rewrite drafts, strategy notes, and optimization guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
