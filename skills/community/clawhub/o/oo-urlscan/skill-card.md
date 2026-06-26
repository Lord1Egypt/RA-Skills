## Description: <br>
Operate urlscan.io through the OOMOL oo CLI for retrieving completed scan results, searching scans, and submitting URLs for scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security analysts use this skill to interact with urlscan.io from an agent workflow through an OOMOL-connected account. It supports reading scan results, searching scans, and submitting URLs for scanning after confirming write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OOMOL as the connector layer and requires sensitive urlscan.io credentials. <br>
Mitigation: Install only when that connector path is acceptable, review the oo CLI installer before use, and connect a minimally scoped urlscan.io API key. <br>
Risk: Submitting a URL for scanning changes urlscan.io state and may expose the submitted URL to urlscan.io. <br>
Mitigation: Confirm the exact URL submission payload and expected effect with the user before running the write action. <br>
Risk: Authentication, connection, billing, or CLI setup commands can alter the local or account environment. <br>
Mitigation: Run setup steps only after a matching command failure and avoid proactive login, connection, or install actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-urlscan) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [urlscan.io homepage](https://urlscan.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an OOMOL sign-in, and a connected urlscan.io API key; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
