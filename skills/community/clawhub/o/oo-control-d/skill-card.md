## Description: <br>
Control D (controld.com). Use this skill for ANY Control D request: reading, creating, updating, and deleting data through the OOMOL Control D connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Control D profiles and manage custom DNS profile rules through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change persistent Control D DNS profile rules. <br>
Mitigation: Confirm the exact write payload and expected filtering effect with the user before running actions tagged [write]. <br>
Risk: The skill can delete Control D profile rules. <br>
Mitigation: Require explicit user approval for destructive actions and confirm the target rule before deletion. <br>
Risk: The skill depends on OOMOL-connected credentials and the oo CLI provider. <br>
Mitigation: Install and use it only when the user intends to let an agent manage Control D through OOMOL, and run the remote oo CLI installer only when OOMOL is trusted as the provider. <br>


## Reference(s): <br>
- [Control D homepage](https://controld.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-control-d) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Control D profile, rule, service, IP, datacenter, and execution metadata from oo CLI calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
