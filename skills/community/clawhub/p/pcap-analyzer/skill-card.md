## Description: <br>
Analyze PCAP/PCAPNG files with tshark and produce a structured network-forensics summary covering talkers, ports, DNS, TLS, HTTP, and anomalies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marposins](https://clawhub.ai/user/marposins) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security analysts, and network engineers use this skill to summarize local packet captures for lab work, incident triage, and CPENT-style exercises. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured command invokes an unbundled hardcoded local script whose behavior was not available for review. <br>
Mitigation: Inspect and trust /home/tom/openclaw-tools/pcap_summary.sh before use, or change the skill to use the bundled scripts/analyze.sh fallback directly. <br>
Risk: PCAP files and generated reports can expose hostnames, URLs, services, and internal network activity. <br>
Mitigation: Treat input captures and reports as sensitive, keep analysis local, and use read-only access where possible. <br>


## Reference(s): <br>
- [tshark Manual Page](https://www.wireshark.org/docs/man-pages/tshark.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text structured network-forensics report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local PCAP or PCAPNG file path and can optionally focus output on a specified host.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
