## Description: <br>
Audits dependency supply chains for bad versions, lockfile drift, and artifact integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit Python dependency supply chains, check lockfiles and artifacts against known-bad versions, and plan response steps for suspected package compromise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes incident-response automation guidance that can affect credentials, budgets, webhook registration, escrow cancellation, containment, and recovery workflows. <br>
Mitigation: Review thresholds and containment actions before use, test against a sandbox or a single agent, and align actions with the operator's approval process. <br>
Risk: Supply-chain incident guidance can lead to disruptive remediation steps such as stopping processes, changing dependency constraints, regenerating lockfiles, reinstalling environments, and rotating credentials. <br>
Mitigation: Preserve evidence for forensics, validate affected package versions and indicators first, and execute remediation through the organization's incident-response process. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-leyline-supply-chain-advisory) <br>
- [Leyline Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Incident Response Module](artifact/modules/incident-response.md) <br>
- [Scanning Patterns Module](artifact/modules/scanning-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose dependency exclusions, lockfile scans, artifact searches, and incident-response checklists for operator review.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
