## Description: <br>
Configure Tor Browser to access Mobazha stores privately, or run a store as a .onion hidden service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengzie](https://clawhub.ai/user/fengzie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mobazha buyers and store operators use this skill to configure private Tor access for browsing stores and to run Mobazha stores as .onion hidden services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that download and run a Mobazha installer with sudo privileges. <br>
Mitigation: Review the command and source URL before execution, and run it only on the intended host with appropriate administrative authorization. <br>
Risk: The skill discusses cryptocurrency payments and private marketplace browsing. <br>
Mitigation: Confirm purchases and payment methods comply with applicable law, platform rules, and organizational policy before authorizing any transaction. <br>
Risk: Tor routing protects network privacy but does not encrypt stored data. <br>
Mitigation: Use separate data protection controls such as storage encryption, access control, backups, and regular software updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengzie/mobazha-tor-browsing) <br>
- [Tor Browser download](https://www.torproject.org/download/) <br>
- [Mobazha app](https://app.mobazha.org) <br>
- [Mobazha standalone installer](https://get.mobazha.org/standalone) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes buyer browsing guidance and seller hidden-service setup options.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
