## Description: <br>
Empowers AI agents to assess crypto asset vitality by calling the Majestify crypto-health API for risk metrics and vitality classifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MajestyAtenkhu](https://clawhub.ai/user/MajestyAtenkhu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to request crypto asset risk metrics and classify assets as IMMORTAL, MORTAL, CRITICAL, or UNKNOWN for portfolio review workflows. The classifications should support analysis rather than replace financial judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested coin IDs and time-window parameters to an external crypto-health API or another endpoint selected by the user. <br>
Mitigation: Use only trusted API endpoints and avoid custom API URLs that are not explicitly approved. <br>
Risk: Crypto vitality classifications and risk metrics may be mistaken for automatic investment instructions. <br>
Mitigation: Treat results as analytical signals for human review, not as standalone financial advice or trading decisions. <br>


## Reference(s): <br>
- [ClawHub Immortal release page](https://clawhub.ai/MajestyAtenkhu/immortal) <br>
- [Majestify](https://majestify.io) <br>
- [Crypto Health Hub API](https://crypto-health-hub.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable terminal text on stdout with machine-readable JSON on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires internet access to the configured API endpoint; httpx is optional and urllib is used as a fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
