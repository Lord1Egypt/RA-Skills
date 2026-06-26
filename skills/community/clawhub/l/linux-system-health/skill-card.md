## Description: <br>
Diagnose Linux OS-level issues - slow server, OOM kills, disk full, high CPU/load, DNS failures, connection timeouts, port exhaustion, too many open files, zombie processes, browser automation failures, locale problems, and kernel misconfigurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjxylc](https://clawhub.ai/user/zjxylc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system operators use this skill to diagnose Linux server health issues, identify OS-level root causes, and produce severity-ranked remediation guidance for memory, CPU, disk, network, kernel, process, browser dependency, and locale problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Root execution can expose or affect sensitive Linux server state. <br>
Mitigation: Review the shell script before running it as root and execute only the sections relevant to the reported symptoms when possible. <br>
Risk: Diagnostic output can contain process names, socket owners, kernel messages, configuration details, and selected OOM-related log lines. <br>
Mitigation: Treat diagnostic output as sensitive operational data and redact it before sharing outside trusted support channels. <br>
Risk: The DNS nameserver reachability check can run shell code from malformed resolver data according to the authoritative security summary. <br>
Mitigation: Fix or inspect that command path before running the DNS section on systems where resolver configuration may be untrusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zjxylc/linux-system-health) <br>
- [Homepage](https://github.com/ecsgo-helper/openclaw-system-health) <br>
- [Issue registry and severity reference](reference.md) <br>
- [Server-resolved provenance](unavailable) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and severity-sorted diagnostic findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Linux-only; diagnostic output can include process names, socket owners, kernel messages, configuration details, and selected OOM-related log lines.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
