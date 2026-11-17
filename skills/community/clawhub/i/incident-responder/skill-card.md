## Description:

Playbook-driven incident response for MITRE ATT&CK mapping, evidence collection, timeline reconstruction, containment procedures, and post-incident reporting with ARGUS and BlackArch tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1beekeeper](https://clawhub.ai/user/1beekeeper)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, incident responders, and developers use this skill to guide triage, evidence collection, timeline reconstruction, containment, and reporting for suspected data exfiltration, ransomware, and credential compromise incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful system-wide evidence collection and containment commands could expose sensitive data or disrupt a host if run without careful review.

Mitigation: Treat commands as operator-reviewed snippets and confirm the host, incident scope, account and IP targets, evidence location, retention policy, and rollback plan before execution.

Risk: Incident evidence directories may contain sensitive logs, memory captures, packet captures, credentials, or regulated data.

Mitigation: Store evidence in restricted directories, preserve chain of custody, and use restrictive permissions and encryption appropriate to the incident.

## Reference(s):

- [Incident Responder ClawHub Skill Page](https://clawhub.ai/1beekeeper/skills/incident-responder)
- [ARGUS Homepage](https://github.com/nousresearch/argus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks, command templates, playbooks, and incident report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux-oriented ARGUS workflows requiring curl, jq, grep, awk, and optional forensics tools; examples may require operator-approved root or sudo access.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
