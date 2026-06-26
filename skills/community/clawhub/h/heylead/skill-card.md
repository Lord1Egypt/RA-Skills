## Description: <br>
HeyLead connects an OpenClaw agent to an MCP-native LinkedIn SDR that supports prospecting, personalized outreach, follow-up, reply handling, and pipeline tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[D4umak](https://clawhub.ai/user/D4umak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales teams and go-to-market operators use HeyLead to connect an OpenClaw agent to LinkedIn outreach workflows. It helps create buyer personas and campaigns, send or review personalized messages, monitor replies, and track pipeline outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous LinkedIn account actions could send outreach or engagement without sufficient review. <br>
Mitigation: Start in Copilot/review mode, keep the cloud scheduler disabled until safeguards are understood, and use pause or emergency-stop controls for active campaigns. <br>
Risk: The security evidence says approval, token, and scheduler boundaries are not clear enough. <br>
Mitigation: Pin and inspect the heylead package before use, verify how to revoke Google and LinkedIn access, and avoid sensitive conversations unless the local storage and external AI processing model is acceptable. <br>


## Reference(s): <br>
- [HeyLead ClawHub release](https://clawhub.ai/D4umak/heylead) <br>
- [HeyLead PyPI project](https://pypi.org/project/heylead/) <br>
- [HeyLead GitHub repository](https://github.com/D4umak/heylead) <br>
- [HeyLead issue tracker](https://github.com/D4umak/heylead/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and natural-language command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure an MCP server that can operate a user's LinkedIn account after account setup.] <br>

## Skill Version(s): <br>
0.9.13 (source: server release metadata and artifact clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
