## Description:

Property Advisor orchestrates property search, screening, comparison, map enrichment, profile memory, watched listings, and listing publishing workflows through upstream source adapters and a bundled public OSM map-context skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongzzzzzzzzz](https://clawhub.ai/user/dongzzzzzzzzz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and property operators use the skill to search, compare, shortlist, and monitor property listings, enrich candidates with map context, and prepare listing-publishing readiness reports before confirmed submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run auto-discovered upstream OK/GT skill code.

Mitigation: Set explicit trusted OK/GT skill roots, avoid untrusted workspaces, and review upstream skills before use.

Risk: The skill can keep local housing preferences, searches, watched listings, and map cache data.

Mitigation: Use --no-memory for private searches and clear ~/property-advisor/ and the OSM cache when local state should not persist.

Risk: Publishing workflows can prepare payloads for real listing submission.

Mitigation: Review every publishing payload and use real submission only after explicit confirmation with --confirm-submit.

Risk: Public OSM map context is best-effort and may be incomplete, unavailable, or only area-level.

Mitigation: Treat OSM enrichment as screening support, use manual verification links for final checks, and avoid precise listing-level distance claims when only area-level evidence is available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongzzzzzzzzz/skills/property-advisor)
- [Upstream Sources](references/upstream-sources.md)
- [Map Context Contract](references/map-context-contract.md)
- [Data Contract](references/data-contract.md)
- [Output Contract](references/output-contract.md)
- [Response Examples](references/response-examples.md)
- [Public OSM Map Context Skill](public-osm-map-context-skill/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown decision tables and JSON reports, with shell commands for deterministic CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search outputs preserve original listing URLs; publishing workflows default to dry-run/readiness reporting and require explicit confirmation for real submission.]

## Skill Version(s):

3.1.2 (source: ClawHub release evidence; artifact pyproject.toml reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
