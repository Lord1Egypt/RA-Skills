## Description: <br>
Kiln lets AI agents design, slice, print, monitor, and recover 3D printer jobs through MCP and CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeofaxel](https://clawhub.ai/user/codeofaxel) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers, makers, and fabrication operators use Kiln to connect AI agents to 3D printers, slicers, model marketplaces, and fulfillment workflows. Agents can generate or find models, validate files, queue jobs, monitor cameras, estimate costs, and manage printer fleets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can control physical 3D printers, including starting, pausing, canceling, and sending validated G-code. <br>
Mitigation: Use only with working firmware safety limits, accessible emergency stop or power cutoff, verified printer profiles, and supervised first runs. <br>
Risk: Camera monitoring and printer/API credentials may expose sensitive workspace images or access tokens. <br>
Mitigation: Review camera behavior and credential storage before use, keep printer/API keys scoped, and enable authentication controls where available. <br>
Risk: Marketplace, fulfillment, wallet, and purchase-related capabilities can create spending or transaction exposure. <br>
Mitigation: Require human confirmation for orders or payments and verify fulfillment spending limits before allowing autonomous use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeofaxel/kiln) <br>
- [Kiln documentation](https://kiln3d.com/docs) <br>
- [Kiln website](https://kiln3d.com) <br>
- [PyPI package](https://pypi.org/project/kiln3d/) <br>
- [Declared repository](https://github.com/codeofaxel/Kiln) <br>
- [Release v1.1.8](https://github.com/codeofaxel/Kiln/releases/tag/v1.1.8) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and MCP/CLI action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference printer credentials, camera snapshots, marketplace searches, fulfillment quotes, and confirmation-gated printer actions.] <br>

## Skill Version(s): <br>
1.1.8 (source: server.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
