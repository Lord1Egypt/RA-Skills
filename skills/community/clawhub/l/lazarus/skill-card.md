## Description:

Lazarus v2 helps agents discover evidence-backed dead domains or verify a supplied domain, recover archived pages with heuristic indexing evidence, pass a review gate, and package a machine-readable Recovery Bundle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsorgcn](https://clawhub.ai/user/adsorgcn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content operators use Lazarus to find dead websites worth recovering, verify domain death, recover Wayback snapshots, and produce rewrite-source notes, private corpus files, or republish-ready Markdown only after review gates pass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may query public search engines, Wayback, or optional keyed search providers and may write recovered website bundles.

Mitigation: Validate targets before network access, sanitize URLs before external queries, require user confirmation before recovery, and apply the documented rate limits.

Risk: Recovered content may carry copyright or trademark risk, especially when using republish mode.

Mitigation: Use rewrite_source by default, avoid copying original expression, and require explicit copyright-risk acknowledgment before public republishing.

Risk: Archived pages can contain PII, secrets, internal endpoints, or unsafe identifiers.

Mitigation: Run the review gate on produced content, keep PII scanning enabled, redact findings, and fail the gate when secrets are found.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adsorgcn/skills/lazarus)
- [iLang Homepage](https://ilang.ai)
- [AutoCode](https://github.com/ilang-ai/autocode)
- [OpenClaw Skills](https://github.com/ilang-ai/ilang-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown plus machine-readable JSON and JSONL Recovery Bundle files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default rewrite_source mode produces source notes without copied full text; republish and private_corpus can produce full Markdown with review reports and deploy notes only when gates allow.]

## Skill Version(s):

2.0.2 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
