## Description: <br>
Hyperspace helps an agent install and use the Hyperspace distributed AI network for autonomous research, P2P inference, node status, model management, and points tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twobitapps](https://clawhub.ai/user/twobitapps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to join and manage a Hyperspace node, run autonomous research workflows, route suitable requests to distributed inference, and inspect models, status, research results, and points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and starts persistent P2P compute software immediately. <br>
Mitigation: Review the installer source before execution, confirm how to stop and remove the service, and only proceed if persistent network participation is acceptable. <br>
Risk: Node participation may consume CPU, GPU, and network resources. <br>
Mitigation: Check expected resource usage and monitor the node after installation with status and system information commands. <br>
Risk: The node shares peer identity, capabilities, and experiment metrics with the network. <br>
Mitigation: Confirm the metadata sharing model and remove the service and local identity if the disclosed data is not acceptable. <br>


## Reference(s): <br>
- [Hyperspace homepage](https://hyper.space) <br>
- [Hyperspace node source](https://github.com/hyperspaceai/hyperspace-node) <br>
- [Hyperspace node releases](https://github.com/hyperspaceai/hyperspace-node/releases) <br>
- [Hyperspace install script](https://github.com/hyperspaceai/hyperspace-node/blob/main/install.sh) <br>
- [Hyperspace CLI installer](https://agents.hyper.space/cli) <br>
- [ClawHub skill page](https://clawhub.ai/twobitapps/hyperspace) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for installing, starting, checking, updating, and removing a persistent Hyperspace node.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
