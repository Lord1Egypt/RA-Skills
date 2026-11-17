## Description:

Verify academic paper citations using local FTS5 data, Semantic Scholar, and OpenAlex, with support for single citation checks and batch reference-list audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diamond2nv](https://clawhub.ai/user/diamond2nv)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, reviewers, literature-survey authors, and agents use this skill to check whether cited academic papers exist and to audit reference lists for missing, suspected, or verified citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto mode may send citation titles, arXiv IDs, and author or year hints to Semantic Scholar or OpenAlex.

Mitigation: Use local source mode for confidential bibliographies when possible, and review citation inputs before enabling network-backed sources.

Risk: Optional extras and MCP registration can broaden the runtime surface beyond basic citation checks.

Mitigation: Review optional extras and MCP configuration before enabling them in an agent environment.

Risk: Anonymous academic API tiers can be rate-limited, which may produce ERROR statuses or slower audits.

Mitigation: Use the local FTS5 source where available, or configure the documented Semantic Scholar and OpenAlex rate-limit options for higher-volume use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diamond2nv/skills/hfpclawer-citation-audit)
- [Project homepage](https://github.com/diamond2nv/hfpapers-crawler)
- [PyPI package](https://pypi.org/project/hfpclawer/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples and citation-status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report VERIFIED, SUSPECTED, NOT_FOUND, or ERROR statuses and include source-specific results.]

## Skill Version(s):

0.19.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
