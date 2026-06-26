## Description: <br>
Security audit and threat model for OpenClaw gateway hosts. Use to verify OpenClaw configuration, exposure, skills/plugins, filesystem hygiene, and to produce an OK/VULNERABLE report with evidence and fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misirov](https://clawhub.ai/user/misirov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to audit OpenClaw gateway host configuration, exposure, skills and plugins, filesystem hygiene, and related threat paths. It produces an evidence-based OK/VULNERABLE report with severity and fix guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs an agent to run scripts/collect_verified.sh immediately, but the release artifact only includes SKILL.md and does not bundle that script. <br>
Mitigation: Do not run the collection script unless the exact script and referenced files are obtained from a trusted source, reviewed, and explicitly approved from a trusted working directory. <br>
Risk: The requested audit depends on local evidence collection and may expose sensitive host, configuration, or credential-adjacent data if collection behavior is not reviewed. <br>
Mitigation: Review the collection scope before installation and confirm that tokens, passwords, cookies, OAuth credentials, pairing codes, session contents, and authorization headers are redacted from outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/misirov/macarena-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown security audit report with evidence excerpts, findings, threat model, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a verified evidence bundle and redacts secrets from reported excerpts.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
