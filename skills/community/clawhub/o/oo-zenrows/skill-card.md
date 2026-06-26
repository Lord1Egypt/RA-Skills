## Description: <br>
ZenRows (zenrows.com) helps agents fetch raw HTML, extract plain text, extract CSS-selected structured values, and retrieve usage details through an OOMOL-connected ZenRows account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve webpage HTML or text, extract structured values with CSS selectors, and check ZenRows usage through the oo CLI without handling raw ZenRows API tokens directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance includes unverified remote installer commands for the oo CLI. <br>
Mitigation: Review the installer source first, prefer official version-pinned and checksum- or signature-verified installation steps, and do not let an agent run remote install commands automatically. <br>
Risk: The skill requires a connected ZenRows account and sensitive credentials managed outside the skill. <br>
Mitigation: Install and authenticate the oo CLI yourself, connect ZenRows explicitly, and let agents run only the documented connector actions after setup succeeds. <br>


## Reference(s): <br>
- [ZenRows homepage](https://www.zenrows.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-zenrows) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions return connector JSON responses that include data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
