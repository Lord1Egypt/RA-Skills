## Description: <br>
Connect to Komandr Command Center to receive tasks, report progress, and submit work results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emersonaidev](https://clawhub.ai/user/emersonaidev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an OpenClaw agent to Komandr Command Center so the agent can receive assigned tasks, report status, and submit work results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A remote Komandr service can assign broad work to the agent and influence what actions it takes. <br>
Mitigation: Use only a trusted Komandr instance, verify KOMANDR_URL before use, and review tasks before accepting or executing them. <br>
Risk: Task results or artifacts may send work details, file contents, logs, or other sensitive data off-system. <br>
Mitigation: Do not submit secrets, private source files, logs, customer data, or credentials unless the Komandr server is approved to receive them. <br>
Risk: The bridge depends on npx tsx execution and a Komandr API key in the environment. <br>
Mitigation: Preinstall or pin tsx and use a least-privilege API key for the agent. <br>


## Reference(s): <br>
- [Komandr Agent API Reference](references/api-reference.md) <br>
- [Komandr default service URL](https://komandr.vercel.app) <br>
- [ClawHub skill page](https://clawhub.ai/emersonaidev/komandr) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KOMANDR_API_KEY and may use KOMANDR_URL to select the Komandr instance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
