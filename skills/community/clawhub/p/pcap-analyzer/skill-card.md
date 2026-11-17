## Description:

Analyze local PCAP and PCAPNG files with tshark to generate structured network forensics reports covering talkers, conversations, ports, DNS, TLS, HTTP, and anomaly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marposins](https://clawhub.ai/user/marposins)

### License/Terms of Use:


## Use Case:

Security analysts, incident responders, lab users, and network engineers use this skill to summarize local packet captures for triage, investigation, and training exercises.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command entry point can execute unsafe shell input.

Mitigation: Review before installing, use only trusted PCAP paths, and run in a restricted environment until the command uses safe argument-array execution and path handling.

Risk: The skill depends on an unreviewed external summarizer.

Mitigation: Bundle the summarizer or verify it by digest and restrictive ownership before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marposins/skills/pcap-analyzer)
- [TShark manual](https://www.wireshark.org/docs/man-pages/tshark.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text structured network-forensics report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report sections may include capture metadata, top talkers, conversations, service and port summaries, DNS, TLS, HTTP, and best-effort anomaly findings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
