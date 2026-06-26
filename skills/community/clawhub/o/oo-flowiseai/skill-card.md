## Description: <br>
FlowiseAI (flowiseai.com) supports reading, creating, and updating data through an OOMOL-connected FlowiseAI account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect FlowiseAI connector schemas, fetch the protected chatflow, and send JSON prediction requests through the oo CLI. It is intended for users who have connected FlowiseAI to their OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected FlowiseAI account and OOMOL-managed credentials. <br>
Mitigation: Install it only if you trust OOMOL and intend the agent to use your connected FlowiseAI account. <br>
Risk: The send_message action can submit prediction requests to the protected chatflow. <br>
Mitigation: Review and approve the exact JSON payload before running write actions. <br>
Risk: First-time setup may install the oo CLI from an external installer. <br>
Mitigation: Verify the oo CLI installer source before installing in managed or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-flowiseai) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [FlowiseAI homepage](https://flowiseai.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [FlowiseAI connection setup](https://console.oomol.com/app-connections?provider=flowiseai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
