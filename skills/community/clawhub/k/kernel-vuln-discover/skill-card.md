## Description: <br>
Guides agents through proactive Linux kernel vulnerability discovery using subsystem attack-surface enumeration, CVE pattern scanning, fuzzing, static audit, diff analysis, and vulnerability report drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjd6910502](https://clawhub.ai/user/wjd6910502) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security researchers, kernel engineers, and agent developers use this skill to plan and document Linux kernel vulnerability discovery work, including targeted subsystem audits, fuzzing setup, pattern-based scans, and report preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fuzzing workflows, proof-of-concept code, or generated vulnerability reports could be unsafe or misleading if run against production systems or trusted as confirmed findings. <br>
Mitigation: Run fuzzers and PoCs only in isolated VMs or test machines, and manually validate every result before reporting or acting on it. <br>
Risk: Pattern-scan output has a high false-positive rate and may reference CVE patterns that need independent confirmation. <br>
Mitigation: Review the local scan script before use, verify CVE references independently, and confirm code context before treating a hit as a vulnerability. <br>


## Reference(s): <br>
- [CVE Pattern Library](references/cve-patterns.md) <br>
- [Subsystem Audit Checklists](references/subsystem-checklists.md) <br>
- [Trinity syscall fuzzer](https://github.com/kernelsploit/trinity) <br>
- [Linux kernel upstream commit log](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/) <br>
- [ClawHub skill page](https://clawhub.ai/wjd6910502/kernel-vuln-discover) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands, C snippets, YAML snippets, and vulnerability report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes pattern-scan guidance and report structure; scan hits require manual validation before disclosure or remediation work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
