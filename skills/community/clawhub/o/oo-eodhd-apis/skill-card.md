## Description: <br>
EODHD APIs helps agents search and read EODHD market and economic data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query authenticated EODHD market data, instrument metadata, macro indicators, U.S. Treasury yield rates, and account usage through OOMOL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connection to an EODHD API account and may use sensitive account credentials managed by OOMOL. <br>
Mitigation: Install and use the skill only when the user trusts OOMOL and intends to connect an EODHD API account. <br>
Risk: The documented first-time setup includes a remote shell installer for the oo CLI. <br>
Mitigation: Prefer OOMOL's install guide or inspect the installer before executing it, especially in managed or production environments. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/oomol/oo-eodhd-apis) <br>
- [EODHD APIs Homepage](https://eodhd.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated oo CLI plus a connected EODHD APIs account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
