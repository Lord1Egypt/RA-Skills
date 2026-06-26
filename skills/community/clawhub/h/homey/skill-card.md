## Description: <br>
Control Athom Homey smart home devices via local (LAN/VPN) or cloud APIs. List/control devices, trigger flows, query zones. Works with Homey Pro, Cloud, and Bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxsumrall](https://clawhub.ai/user/maxsumrall) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect and control Athom Homey smart-home devices, zones, and flows through local or cloud APIs. It is intended for device listing, state queries, automation triggers, and explicit smart-home control actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: State-changing commands can control physical smart-home devices, including locks, thermostats, lights, appliances, and automation flows. <br>
Mitigation: Confirm the exact device or flow and intended action before execution; prefer snapshot and list commands first, and use extra caution for unlocks, thermostat changes, appliances, and flow triggers. <br>
Risk: Homey local and cloud tokens grant device-control authority. <br>
Mitigation: Enter tokens through prompt or stdin where possible, protect the Homey config file, and avoid shared machines unless file permissions and token scope are acceptable. <br>
Risk: Fuzzy matching can target the wrong device or flow when names are similar or ambiguous. <br>
Mitigation: Use JSON listings and stable IDs for critical actions; review returned candidates when a command reports an ambiguous match. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maxsumrall/homey) <br>
- [homeycli Documentation](https://maxsumrall.github.io/homeycli/) <br>
- [Command Reference](docs/commands.md) <br>
- [Output Contract](docs/output.md) <br>
- [Homey Developer Tools](https://tools.developer.homey.app/api/clients) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration guidance] <br>
**Output Format:** [CLI commands with JSON output when --json is used, plus human-readable terminal text for non-JSON commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stable JSON success and error envelopes are documented for agent use; state-changing commands can affect real Homey devices and flows.] <br>

## Skill Version(s): <br>
1.1.2 (source: package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
