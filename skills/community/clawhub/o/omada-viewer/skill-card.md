## Description: <br>
Read-only diagnostics for TP-Link Omada SDN controllers via the Open API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjuff](https://clawhub.ai/user/imjuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators and support engineers use this skill to inspect Omada controller health, devices, clients, VLANs, WAN status, ports, DHCP ranges, and port forwards for troubleshooting and inventory without making configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is described as a read-only diagnostics helper, but the bundled all-endpoints catalog includes broad write and admin API routes. <br>
Mitigation: Use only the documented read-only diagnostics commands with a dedicated Viewer-scoped Omada Open API app, and remove or separately gate write, delete, reboot, and admin routes before normal viewer use. <br>
Risk: Omada API credentials and relaxed SSL verification can expose controller access if handled carelessly. <br>
Mitigation: Keep secrets out of chat and logs, store them locally, and leave SSL verification enabled unless the local controller setup is fully trusted. <br>


## Reference(s): <br>
- [Omada Northbound API Endpoints Reference](references/api-endpoints.md) <br>
- [Practical Omada Endpoints](references/discovered-endpoints.md) <br>
- [Omada Controller API Endpoints](references/all-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and text or JSON diagnostic output from the Omada query script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Omada Open API credentials and HTTPS access to the user's controller.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
