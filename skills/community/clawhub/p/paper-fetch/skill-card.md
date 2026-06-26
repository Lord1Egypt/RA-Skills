## Description: <br>
Use when the user wants to download a paper PDF from a DOI or title, with fallback across Unpaywall, arXiv, bioRxiv/medRxiv, PubMed Central, Semantic Scholar, and Sci-Hub mirrors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, developers, and research-support agents use Paper Fetch to resolve DOIs or paper titles and download PDFs through a deterministic source chain. It supports single-paper and batch workflows with structured output for automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill silently self-updates from git on first use, which can change behavior after review. <br>
Mitigation: Disable or remove the auto-update behavior and pin the skill to a reviewed commit or release before installing. <br>
Risk: Sci-Hub fallback is enabled by default and may retrieve content outside authorized or open-access sources. <br>
Mitigation: Set PAPER_FETCH_NO_SCIHUB=1 when operators only want authorized or open-access sources. <br>
Risk: Institutional mode uses the operator's institutional access and may create publisher policy risk if used for broad downloads. <br>
Mitigation: Enable PAPER_FETCH_INSTITUTIONAL=1 only when permitted by the institution, preserve the built-in rate limiting, and use the workflow for scoped research tasks. <br>
Risk: Downloaded PDFs are written to a local output directory selected by the caller. <br>
Mitigation: Use a scoped output directory for downloads and review generated files before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/agents365-ai/paper-fetch) <br>
- [README.md](README.md) <br>
- [Documentation](docs/index.html) <br>
- [Unpaywall](https://unpaywall.org) <br>
- [Semantic Scholar](https://www.semanticscholar.org) <br>
- [arXiv](https://arxiv.org) <br>
- [PubMed Central](https://pmc.ncbi.nlm.nih.gov) <br>
- [bioRxiv](https://www.biorxiv.org) <br>
- [medRxiv](https://www.medrxiv.org) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, NDJSON progress, downloaded PDF files, guidance] <br>
**Output Format:** [JSON envelope on stdout, NDJSON progress on stderr, and PDF files in the selected output directory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry runs, batch mode, idempotency keys, typed exit codes, retry hints, and a schema subcommand.] <br>

## Skill Version(s): <br>
0.13.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
