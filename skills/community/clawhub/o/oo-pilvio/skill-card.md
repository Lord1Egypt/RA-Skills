## Description: <br>
Pilvio helps an agent read Pilvio account, billing, location, and virtual machine data through an OOMOL-connected account using the oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with OOMOL-connected Pilvio accounts use this skill to inspect Pilvio user profile, billing account, data center location, and virtual machine information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance may ask the user to run remote installer scripts for the oo CLI. <br>
Mitigation: Run installer commands only after intentional user approval and only from the documented OOMOL CLI install locations. <br>
Risk: The skill reads Pilvio account data through the user's connected OOMOL account. <br>
Mitigation: Use it only for intended read-only Pilvio profile, billing, location, and virtual machine queries, and handle returned account data as sensitive. <br>


## Reference(s): <br>
- [Pilvio homepage](https://pilvio.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-pilvio) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector runs return JSON data with execution metadata when commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
