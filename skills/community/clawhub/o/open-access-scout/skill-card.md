## Description:

Use when finding open access journals, checking journal policies, or identifying predatory publishers. Helps researchers locate legitimate open access venues and avoid publication scams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, librarians, and research-support teams use this skill to identify open access venues, check publication-access options, and surface warning signs before relying on a journal or publisher.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mock open-access results can be mistaken for verified publication-access findings.

Mitigation: Treat outputs as illustrative until the search logic is connected to trusted sources and validated against real DOI or title queries.

Risk: The listed Sci-Hub source can encourage legally or institutionally prohibited access paths.

Mitigation: Remove Sci-Hub from recommended sources and restrict guidance to legitimate open-access services and repository checks.

Risk: Claims about journal legitimacy, policies, APCs, and predatory publishers may exceed the implemented script.

Mitigation: Use outputs as preliminary guidance and verify journal status, indexing, APCs, and policies against authoritative publisher and index sources before acting.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [Open Access Scout on ClawHub](https://clawhub.ai/aipoch-ai/skills/open-access-scout)
- [Unpaywall](https://api.unpaywall.org/)
- [CORE](https://core.ac.uk/)
- [PubMed Central](https://www.ncbi.nlm.nih.gov/pmc/)
- [arXiv](https://arxiv.org/)
- [bioRxiv](https://www.biorxiv.org/)
- [medRxiv](https://www.medrxiv.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional CLI commands and structured result sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, limits, risks, unresolved items, and validation needs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
