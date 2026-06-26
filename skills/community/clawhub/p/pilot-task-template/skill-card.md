## Description: <br>
Reusable task templates with placeholder substitution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to define reusable Pilot Protocol task templates, substitute variables, and submit standardized task descriptions with pilotctl. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated task text may be incorrect, misleading, or unintended before it is sent to an external agent. <br>
Mitigation: Review instantiated task text before submission through pilotctl. <br>
Risk: Saved templates or template variables may contain credentials, tokens, sensitive prompts, or other private data. <br>
Mitigation: Keep ~/.pilot/templates under user control and avoid storing secrets or sensitive prompts in templates or variables. <br>
Risk: The workflow depends on Pilot Protocol tooling and a running daemon. <br>
Mitigation: Install and trust Pilot Protocol, ensure pilotctl is on PATH, and start the daemon before using the generated commands. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-task-template) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reusable task-template patterns and pilotctl submission commands; generated task text should be reviewed before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
