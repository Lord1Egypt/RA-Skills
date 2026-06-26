## Description: <br>
Bouncer helps agents verify emails and domains, manage Bouncer batch verification and toxicity-list jobs, and check Bouncer credits through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run Bouncer email verification, domain verification, batch verification, toxicity-list, and credit-check workflows through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup may require installing the oo CLI with a remote shell or PowerShell installer. <br>
Mitigation: Review the official OOMOL CLI installer or install guide before running it, and only install from the documented OOMOL URLs. <br>
Risk: The skill connects to a Bouncer API-key-backed OOMOL account. <br>
Mitigation: Install only when the user trusts OOMOL and has intentionally connected Bouncer with the required account permissions. <br>
Risk: Batch creation, toxicity-list creation, and batch-sync verification can change Bouncer state or consume account credits. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: Delete actions can remove stored Bouncer batch or toxicity-list results. <br>
Mitigation: Confirm the target identifier and get explicit approval before running destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/oomol/oo-bouncer) <br>
- [Bouncer homepage](https://www.usebouncer.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns oo CLI command guidance, connector schemas, JSON responses, setup steps, and confirmation prompts for write or destructive actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
