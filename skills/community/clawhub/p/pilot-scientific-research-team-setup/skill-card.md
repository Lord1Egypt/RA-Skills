## Description: <br>
Deploy a scientific research team with four agents for literature review, hypothesis generation, experimentation, and reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research teams use this skill to configure a four-agent Pilot Protocol workflow for collaborative scientific research, including literature synthesis, hypothesis ranking, experiment validation, and report preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report role can publish research reports to external destinations. <br>
Mitigation: Decide what research data may leave the environment, restrict destinations where possible, and manually review reports before external publication. <br>
Risk: The setup depends on pilotctl, clawhub, and listed pilot-* skills that affect multi-agent communication. <br>
Mitigation: Install only trusted versions of these tools and skills, then verify trust relationships before exchanging research data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-scientific-research-team-setup) <br>
- [Pilot Protocol Homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON manifest examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilot-protocol skill, pilotctl binary, clawhub binary, and a running daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
