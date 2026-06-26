## Description: <br>
Full access to ioBroker via the iobroker simple-api adapter. Read states, objects, historical data, write to states, execute scripts, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanwebgit](https://clawhub.ai/user/sanwebgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home operators use this skill to let an agent inspect, update, and automate ioBroker states through the simple-api adapter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad ioBroker control, including device state changes and script execution. <br>
Mitigation: Install only where agent administrative control over ioBroker is intended, and prefer a restricted ioBroker account with network-limited access. <br>
Risk: Delete and exec/eval operations can make destructive changes or run code in ioBroker. <br>
Mitigation: Avoid or disable delete and exec/eval workflows unless they are explicitly required and reviewed before execution. <br>
Risk: The security summary flags weak scoping and potentially misleading read-only framing. <br>
Mitigation: Treat the release as a high-privilege control integration and document the allowed command scope before deployment. <br>


## Reference(s): <br>
- [ioBroker](https://www.iobroker.net/) <br>
- [ioBroker simple-api Adapter](https://github.com/ioBroker/ioBroker.simple-api) <br>
- [ioBroker REST API Docs](https://www.iobroker.net/#en/adapters/adapterref/iobroker.simple-api/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, configuration] <br>
**Output Format:** [Command responses containing ioBroker state data, object data, status text, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected command and the connected ioBroker simple-api adapter.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
