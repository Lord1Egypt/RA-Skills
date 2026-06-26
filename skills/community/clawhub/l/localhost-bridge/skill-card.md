## Description: <br>
Bridge Docker containers to host localhost services via socat so containerized AI agents can reach services bound to 127.0.0.1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superWorldSavior](https://clawhub.ai/user/superWorldSavior) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and administrators use this skill to plan and manually apply Docker-to-host networking bridges for containerized agents and services that need access to localhost-bound host services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides persistent Linux host-networking changes through systemd services and UFW rules. <br>
Mitigation: Review the generated service, Docker bridge interface, bind address, port, and firewall rule before running commands, and remove the service and rule when they are no longer needed. <br>
Risk: A wrong bind address, bridge interface, or firewall rule could expose a localhost service beyond the intended container network. <br>
Mitigation: Confirm the service binds only to the Docker gateway IP, verify the rule is scoped to the expected bridge interface, and test that the port is not reachable from the public network. <br>


## Reference(s): <br>
- [The Localhost Trap](https://casys.ai/blog/the-localhost-trap) <br>
- [Docker packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires manual administrator review before any host networking changes are applied.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
