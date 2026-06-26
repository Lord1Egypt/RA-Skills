## Description: <br>
Serpdog enables an agent to search and read Google Search, News, Videos, Autocomplete, and account quota data through an OOMOL-connected Serpdog account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run Serpdog-backed search and account lookup actions through the oo CLI without handling raw Serpdog API tokens directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Serpdog API key connected through OOMOL. <br>
Mitigation: Confirm the user trusts OOMOL and intends to connect Serpdog before using the connector. <br>
Risk: First-time setup may require running a remote oo CLI installer if the CLI is missing. <br>
Mitigation: Review the installer source before running it, or use an already installed and trusted oo CLI. <br>


## Reference(s): <br>
- [Serpdog homepage](https://serpdog.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-serpdog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include oo CLI commands, JSON payloads, and JSON connector responses returned by Serpdog actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
