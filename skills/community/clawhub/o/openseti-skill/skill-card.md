## Description: <br>
OpenSETI helps users register a wallet and run SETI-style scans against work units from the OpenSETI network, using signal-processing criteria described in the skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[synergysize](https://clawhub.ai/user/synergysize) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure and run a command-line distributed SETI scanner, submit analysis results, and view contribution stats or leaderboard data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner depends on a private coordinator that controls work downloads and wallet or reward tracking. <br>
Mitigation: Run it only when you trust the publisher and coordinator, and use a wallet address you are comfortable associating with this activity. <br>
Risk: Continuous scanning can create ongoing CPU and network usage. <br>
Mitigation: Use continuous mode only when sustained background compute and network activity are intended. <br>
Risk: Wallet registration may expose a public wallet address to the coordinator. <br>
Mitigation: Provide only a public wallet address and do not enter private keys, seed phrases, or other wallet secrets. <br>


## Reference(s): <br>
- [Breakthrough Listen Open Data Archive](https://breakthroughinitiatives.org/opendatasearch) <br>
- [OpenSETI ClawHub Release](https://clawhub.ai/synergysize/openseti-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides command-line registration, scanning, stats, and leaderboard workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
