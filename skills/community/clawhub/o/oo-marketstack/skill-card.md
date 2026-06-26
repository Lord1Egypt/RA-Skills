## Description: <br>
Marketstack (marketstack.com). Use this skill for ANY Marketstack request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query Marketstack data through an OOMOL-connected account. It supports latest and historical end-of-day market data, ticker profiles, ticker search, currencies, and exchange listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected Marketstack account and may depend on sensitive credentials managed outside the prompt. <br>
Mitigation: Use the OOMOL connection flow, review requested permissions, and provide credentials only when they are required for Marketstack access. <br>
Risk: Generated shell commands could fail or run with an unexpected payload if the connector schema has changed. <br>
Mitigation: Inspect the live connector schema before running actions and use JSON payloads that match the returned contract. <br>
Risk: Authentication, connection, or billing failures may require user account actions before data can be retrieved. <br>
Mitigation: Run setup, reconnect, or billing steps only after the related command fails with the matching error. <br>


## Reference(s): <br>
- [Marketstack homepage](https://marketstack.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-marketstack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, text, and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; action responses are expected as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
