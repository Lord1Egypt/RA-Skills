## Description:

Use when the user wants to download a paper PDF from a DOI or title, resolving titles to DOIs and trying Unpaywall, arXiv, bioRxiv/medRxiv, PubMed Central, Semantic Scholar, and Sci-Hub mirrors as a last-resort fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-focused agent users use this skill to fetch paper PDFs from DOIs, resolve titles to DOIs, run batch downloads, and receive structured results and retry guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sci-Hub fallback is enabled by default and may create legal or policy risk.

Mitigation: Disable it with PAPER_FETCH_NO_SCIHUB=1 unless the operator has reviewed and accepted that behavior.

Risk: The skill can silently self-update from Git before use.

Mitigation: Deploy pinned, reviewed versions and prevent automatic self-updates in managed environments.

Risk: Optional personal or institutional email and access settings may expose operator identity or subscription context.

Mitigation: Set UNPAYWALL_EMAIL or PAPER_FETCH_INSTITUTIONAL only when needed and approved for the operating environment.

## Reference(s):

- [Paper Fetch ClawHub page](https://clawhub.ai/agents365-ai/skills/paper-fetch)
- [Paper Fetch documentation](https://agents365-ai.github.io/paper-fetch/)
- [Unpaywall](https://unpaywall.org)
- [Semantic Scholar](https://www.semanticscholar.org)
- [arXiv PDF endpoint](https://arxiv.org/pdf/{arxiv_id}.pdf)
- [PubMed Central OA](https://pmc.ncbi.nlm.nih.gov)
- [bioRxiv](https://www.biorxiv.org)
- [medRxiv](https://www.medrxiv.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill's CLI emits JSON envelopes on stdout, NDJSON progress on stderr, downloaded PDF files, exit codes, and retry hints.]

## Skill Version(s):

0.13.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
