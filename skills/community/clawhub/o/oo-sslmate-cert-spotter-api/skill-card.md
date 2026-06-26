## Description: <br>
Cert Spotter (sslmate.com) supports reading, creating, updating, and deleting Cert Spotter data through the OOMOL Cert Spotter connector instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Cert Spotter connector schemas, run Cert Spotter account actions, manage monitored domains, and look up certificate issuances through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Cert Spotter API key connected through OOMOL. <br>
Mitigation: Install and use it only when the user trusts OOMOL and approves connecting Cert Spotter credentials through the OOMOL account connector. <br>
Risk: Create, update, and delete actions can change monitored-domain configuration. <br>
Mitigation: Require explicit user confirmation of the target, payload, and expected effect before running any write or destructive action. <br>
Risk: The first-time setup path includes remote installer commands. <br>
Mitigation: Run installer commands only after the oo CLI is missing and the user trusts the source. <br>


## Reference(s): <br>
- [Cert Spotter homepage](https://sslmate.com/certspotter/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-sslmate-cert-spotter-api) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, an authenticated OOMOL account, and a connected Cert Spotter API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
