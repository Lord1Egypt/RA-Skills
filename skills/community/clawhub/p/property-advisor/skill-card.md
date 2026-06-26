## Description: <br>
Property search, screening, comparison, map enrichment, profile memory, watched listings, and listing publishing orchestration for rent, buy, compare, shortlist, commute, amenity, neighborhood-risk, preference-memory, watch-listing, and property-publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongzzzzzzzzz](https://clawhub.ai/user/dongzzzzzzzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, agents, and property operators use this skill to search, screen, compare, and monitor property listings, enrich them with public map context, and prepare property listing publication drafts through upstream listing skills. It is designed as an orchestration layer that normalizes upstream listing results into fixed decision outputs rather than as a native property portal crawler. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store housing preferences and search history in local profile memory. <br>
Mitigation: Use --no-memory or a temporary --memory-dir for sensitive searches, and avoid storing passwords, bank details, contracts, or other highly sensitive documents. <br>
Risk: Address, location, or listing contact details may be sent to public map services or upstream listing skills during enrichment and publishing flows. <br>
Mitigation: Skip map enrichment when location privacy matters and review any upstream account, session, or credential requirements before running listing workflows. <br>
Risk: Publishing workflows can prepare listing content and route to upstream submit flows. <br>
Mitigation: Review generated listing fields, contact details, and readiness reports, and only proceed with real submission after explicit user confirmation. <br>
Risk: The skill orchestrates upstream property sources and does not itself guarantee full-market listing coverage. <br>
Mitigation: Treat results as available-source screening, verify original listing URLs, and avoid assuming all external platforms were searched unless their adapters actually ran. <br>


## Reference(s): <br>
- [Data Contract](references/data-contract.md) <br>
- [Output Contract](references/output-contract.md) <br>
- [Map Context Contract](references/map-context-contract.md) <br>
- [Upstream Sources](references/upstream-sources.md) <br>
- [Decision Dimensions](references/decision-dimensions.md) <br>
- [Region Profiles](references/region-profiles.md) <br>
- [Viewing Checklist](references/viewing-checklist.md) <br>
- [Response Examples](references/response-examples.md) <br>
- [Decision Toolkit](references/decision-toolkit.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and narrative guidance, with JSON-compatible intermediate contracts and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default search output is a fixed eight-column candidate table with original listing URLs, missing facts, risks, and next-step guidance; publishing flows produce readiness reports and draft title or description content before any confirmed submission.] <br>

## Skill Version(s): <br>
3.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
