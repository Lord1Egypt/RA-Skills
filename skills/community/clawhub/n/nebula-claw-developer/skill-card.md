## Description: <br>
Provision, inspect, and terminate disposable OpenNebula virtual machines through a restricted control plane API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ktfh-claw](https://clawhub.ai/user/ktfh-claw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, inspect, and clean up short-lived OpenNebula virtual machines for isolated development, debugging, integration testing, package installation, and risky experiments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and terminate OpenNebula virtual machines, including hard deletion of selected targets. <br>
Mitigation: Use it only in a controlled OpenNebula environment with careful target verification before deletion and clear recording of VM names, IPs, and cleanup status. <br>
Risk: Weak API authentication, network exposure, or credential handling could let infrastructure actions run outside the intended boundary. <br>
Mitigation: Confirm the API is authenticated, bound to localhost or a protected network, uses least-privilege credentials, and avoids plaintext password passing before deployment. <br>
Risk: Uncurated templates, images, or networks could create unsafe or unexpected VM environments. <br>
Mitigation: Restrict the OpenNebula user to documented curated templates, images, and networks, and keep the template allowlist small and reviewed. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Restricted User Setup Reference](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and VM operation details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the API endpoint, VM name, template name, guest IP when available, operation result, and whether the VM was left running or destroyed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
