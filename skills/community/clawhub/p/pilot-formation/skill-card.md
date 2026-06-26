## Description: <br>
Deploy predefined network topologies such as star, ring, mesh, and tree formations for structured swarms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate command-oriented guidance for forming structured Pilot Protocol swarms with predefined communication patterns and trust handshakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill examples automate peer handshakes and approvals, which could establish trust with unintended peers. <br>
Mitigation: Review the peer list manually before approval and avoid approving all pending peers blindly. <br>
Risk: The publish example can disclose swarm name, hub address, and formation time to a configured registry host. <br>
Mitigation: Remove or gate the publish command unless registry disclosure is intentional and the registry host is trusted. <br>
Risk: The skill depends on the Pilot network, pilotctl, a running daemon, and any configured registry host. <br>
Mitigation: Install and run it only in environments where those components are trusted and configured as expected. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-formation) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces topology deployment guidance and shell-command examples for pilotctl-based swarm formation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
