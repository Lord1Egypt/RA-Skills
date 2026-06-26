## Description: <br>
Use this skill for Mezmo requests involving searching or reading account data instead of calling the Mezmo API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Mezmo ingestion status and usage reporting through an OOMOL-connected account. It supports read-only status checks and usage summaries grouped by app, host, or tag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Mezmo account and OOMOL service-mediated credentials. <br>
Mitigation: Install only if you trust OOMOL and are comfortable connecting Mezmo through its service. <br>
Risk: The setup flow includes installing and authenticating the oo CLI. <br>
Mitigation: Review the oo CLI install step before running it and use first-time setup only after an authentication or connection failure. <br>
Risk: Future versions could add actions beyond the currently listed read-only status and usage operations. <br>
Mitigation: Keep the connector scoped to the listed read-only Mezmo actions unless a later release is reviewed and approved. <br>


## Reference(s): <br>
- [Mezmo homepage](https://www.mezmo.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-mezmo) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for read-only Mezmo connector actions; live command responses are JSON from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
