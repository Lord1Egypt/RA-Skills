## Description: <br>
Visualize Pilot Protocol network topology, trust graphs, active connections, and latency maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators working with Pilot Protocol use this skill to inspect peer topology, trust relationships, active connections, and latency using pilotctl output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose network topology, peer, trust, active connection, and latency information from a Pilot Protocol environment. <br>
Mitigation: Use it only in environments where the operator is comfortable allowing an agent to query that Pilot Protocol data through a trusted pilotctl installation. <br>
Risk: Latency checks can generate network traffic. <br>
Mitigation: Run latency queries intentionally and scope them to the nodes needed for the map or investigation. <br>
Risk: The artifact shows jq and Graphviz dot usage even though only pilotctl is declared as a required binary. <br>
Mitigation: Confirm jq and Graphviz are installed before requesting JSON transformations or rendered graph output. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-network-map) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and Graphviz DOT code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to query pilotctl JSON output and render Graphviz diagrams when jq and dot are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
