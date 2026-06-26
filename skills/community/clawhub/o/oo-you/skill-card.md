## Description: <br>
You.com connector helper for searching, fetching webpage content, producing cited research and finance answers, and checking account balance through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route You.com search, content fetching, research, finance research, and account balance requests through the OOMOL oo CLI after inspecting the live connector schema. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected You.com account and may involve sensitive account permissions. <br>
Mitigation: Install and use it only when You.com access through an OOMOL-connected account is intended; review connected account permissions before use. <br>
Risk: First-time setup may require installing the OOMOL oo CLI. <br>
Mitigation: Review the installer path and install the CLI only after an auth, connection, CLI, or credit error requires setup. <br>
Risk: Broad You.com-related requests may select this skill automatically. <br>
Mitigation: Confirm that the requested task should use You.com through OOMOL before running connector actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-you) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [You.com](https://you.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
