## Description: <br>
Instantly.ai lets an agent read, create, and update Instantly.ai campaign and lead data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate an Instantly.ai account from an agent, including listing campaigns and leads, retrieving campaign details, and creating leads after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lead creation changes Instantly.ai marketing data. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: First-time setup can install or authenticate OOMOL tooling and connect an Instantly.ai account. <br>
Mitigation: Run setup steps only after a matching command failure and only when the user trusts the OOMOL tooling and account connection. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-instantly-ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Instantly.ai Homepage](https://instantly.ai) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to fetch live connector schemas before sending JSON payloads and to confirm write actions before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version and skill metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
