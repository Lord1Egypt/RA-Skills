## Description: <br>
Use this skill for Twelve Data (twelvedata.com) requests, including searching and reading data through the OOMOL Twelve Data connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve Twelve Data market information through an OOMOL-connected account. It supports read-only price, quote, profile, time-series, end-of-day, instrument discovery, market mover, and market state lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup may require installing the oo CLI, signing in to OOMOL, connecting a Twelve Data API key, or using OOMOL billing credits. <br>
Mitigation: Only approve setup steps when intentionally configuring this connector, and confirm trust in OOMOL and the oo CLI before installation or login. <br>
Risk: Connector action schemas can define required inputs that are not visible until runtime. <br>
Mitigation: Inspect the live action schema with the oo CLI before constructing a payload, then run the connector with JSON that matches that schema. <br>


## Reference(s): <br>
- [Twelve Data homepage](https://twelvedata.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-twelve-data) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI connector schemas and JSON responses returned by OOMOL.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
