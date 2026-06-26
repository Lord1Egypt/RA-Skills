## Description: <br>
Lianke Print Box helps agents use the lk-print CLI to remotely print, scan, check printer and job status, and manage Lianke cloud print box devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NullYing](https://clawhub.ai/user/NullYing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need agent guidance for Lianke cloud-connected printer and scanner workflows, including authentication, submitting print jobs, polling job state, scanning documents, and checking device status. It is not intended for locally connected printers or non-Lianke devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses API keys, device IDs, and device keys for Lianke cloud printing access. <br>
Mitigation: Treat those values as secrets and avoid sharing them in terminals, logs, chats, screenshots, or generated documents. <br>
Risk: Print and scan jobs may involve confidential documents handled through a cloud-connected device workflow. <br>
Mitigation: Use the skill only when the user trusts the Lianke cloud service, the device owner, and the document handling path. <br>


## Reference(s): <br>
- [Lianke Print Box on ClawHub](https://clawhub.ai/NullYing/lianke-box) <br>
- [lk-print install package](https://github.com/liankenet/lk-print-box.git) <br>
- [Lianke Open Platform](https://open.liankenet.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include lk-print CLI commands, authentication steps, printer or scanner identifiers, task IDs, and JSON-oriented status checks.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
