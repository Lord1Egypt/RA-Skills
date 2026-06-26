## Description: <br>
Valyu lets agents search and read web, academic, financial, and proprietary data through an OOMOL-connected Valyu account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run Valyu searches through the oo CLI with an OOMOL-connected account. The skill retrieves live connector schemas before running actions so search payloads match the current Valyu contract. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Valyu account, so queries and credential-brokered activity may be visible to OOMOL or Valyu. <br>
Mitigation: Install only if OOMOL is an acceptable credential broker for Valyu and avoid submitting sensitive queries unless that data sharing is acceptable. <br>
Risk: Fallback setup commands install the oo CLI from remote installer URLs. <br>
Mitigation: Review the oo CLI installer before running fallback install commands. <br>
Risk: Valyu searches may consume connected-account credits. <br>
Mitigation: Monitor Valyu and OOMOL billing state before retrying searches after billing errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-valyu) <br>
- [Valyu homepage](https://valyu.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs Valyu connector actions through the oo CLI and returns response data with an execution id under meta.executionId.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
