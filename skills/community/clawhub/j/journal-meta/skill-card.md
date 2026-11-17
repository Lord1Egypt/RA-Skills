## Description:

Resolves a paper identifier or title into a metadata record with authors, corresponding author markings, publication details, journal abbreviation, impact factor information, identifiers, citation count, and abstract.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic writing agents use this skill to look up paper metadata from DOI, PMID, arXiv, OpenAlex identifiers, or titles instead of relying on memory. It is suited for citation preparation, author or venue checks, and structured publication metadata retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends paper identifiers or titles to external metadata services during lookup.

Mitigation: Avoid using confidential paper titles, private identifiers, or unpublished research details unless external lookup is acceptable.

Risk: The skill can discover and run local sibling Python CLIs for journal abbreviation and impact-factor enrichment.

Mitigation: Install it only with trusted skills and set JOURNAL_ABBREV_CLI or JOURNAL_IF_CLI only to trusted script paths.

Risk: Returned corresponding authors and impact factors depend on upstream metadata quality and may be missing or approximate.

Mitigation: Review the output sources and treat empty corresponding-author fields or OpenAlex-derived impact factors as metadata limitations, not authoritative absence or official JCR values.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/skills/journal-meta)
- [Project Homepage](https://github.com/Agents365-ai/journal-meta)
- [journal-abbrev](https://github.com/Agents365-ai/journal-abbrev)
- [journal-if](https://github.com/Agents365-ai/journal-if)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with Python CLI commands and JSON or human-readable metadata output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can emit a stable JSON envelope and records metadata sources for returned fields.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
