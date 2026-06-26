## Description: <br>
Censys (censys.com). Use this skill for Censys requests involving searching and reading certificate, host, and web property data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and external agents use this skill to query Censys Global Data through an authenticated OOMOL-connected Censys account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an authenticated OOMOL-connected Censys account and can run CLI commands against that account. <br>
Mitigation: Confirm the target Censys asset and command before execution, and use the connected account flow so raw credentials are not handled in the skill. <br>
Risk: Setup and recovery commands can affect authenticated service state or billing recovery. <br>
Mitigation: Run first-time setup, reconnection, or billing recovery steps only after a command fails with the matching authentication, connection, or credit error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-censys) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Censys homepage](https://censys.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Censys asset data returned as JSON through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
