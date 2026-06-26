## Description: <br>
News API connector skill for searching articles, retrieving top headlines, listing sources, and reading News API data through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query News API through an OOMOL-connected account for article search, top headlines, source discovery, and legacy v1 article compatibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected OOMOL account and News API credentials handled by the connector. <br>
Mitigation: Install and use it only where OOMOL is an approved connector provider for News API access. <br>
Risk: First-time setup may use remote installer commands for the oo CLI. <br>
Mitigation: On sensitive machines, prefer official manual installation or checksum/signature-verified packages before running the CLI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-news-api) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [News API homepage](https://newsapi.org) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to inspect connector schemas and run News API actions; connector responses include data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
