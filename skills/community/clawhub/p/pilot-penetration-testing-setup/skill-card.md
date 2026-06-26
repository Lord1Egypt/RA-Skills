## Description: <br>
Deploy an automated penetration testing pipeline with 4 agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to configure a four-agent penetration testing workflow for reconnaissance, vulnerability scanning, exploit validation, and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures persistent agent state for a penetration testing workflow. <br>
Mitigation: Install only for an approved pentest pipeline and keep a cleanup plan for ~/.pilot/setups/penetration-testing.json, handshakes, and installed role skills. <br>
Risk: The reporter role can send sensitive findings to Slack or webhook destinations. <br>
Mitigation: Confirm destinations are approved, restrict access, and redact exploit evidence where possible before enabling external reporting. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/teoslayer/pilot-penetration-testing-setup) <br>
- [Pilot Protocol Homepage](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup steps, hostname commands, trust handshakes, and setup manifest content.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
