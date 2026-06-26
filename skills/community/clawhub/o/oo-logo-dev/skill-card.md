## Description: <br>
Logo.dev (logo.dev) helps an agent search Logo.dev brand records, retrieve structured brand metadata, and build logo image URLs through the OOMOL `logo_dev` connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to look up Logo.dev brand data or generate logo URLs for domains, brand names, crypto symbols, ISINs, and stock tickers. It is suited for read-oriented brand and logo lookup workflows that rely on an OOMOL-connected Logo.dev account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Logo.dev account and may need first-time CLI installation, login, provider connection, or billing setup. <br>
Mitigation: Treat setup, login, provider connection, and billing actions as user-approved prerequisites, and do not ask users to paste raw credentials into chat. <br>
Risk: Connector schemas and Logo.dev action contracts can change over time. <br>
Mitigation: Fetch the live connector schema before constructing each action payload. <br>
Risk: Logo lookup results may be ambiguous when searching by brand name or query text. <br>
Mitigation: Prefer precise identifiers such as domains, tickers, ISINs, or crypto symbols when available, and have the user confirm candidates before relying on ambiguous search results. <br>


## Reference(s): <br>
- [ClawHub Logo.dev skill](https://clawhub.ai/oomol/oo-logo-dev) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Logo.dev homepage](https://logo.dev) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces read-oriented Logo.dev connector requests and may return structured brand data, logo image URLs, or setup guidance when authentication, connection, or billing prerequisites are missing.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
