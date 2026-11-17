## Description:

Guides agents through proactive Linux kernel vulnerability discovery using subsystem attack-surface enumeration, CVE pattern scanning, fuzzing workflows, static code review, differential analysis, and vulnerability report drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjd6910502](https://clawhub.ai/user/wjd6910502)

### License/Terms of Use:

MIT-0

## Use Case:

Security researchers, kernel engineers, and developers use this skill to plan and execute Linux kernel vulnerability discovery across subsystems such as io_uring, Netfilter, SMB, OverlayFS, BPF, filesystems, and drivers. It helps produce audit plans, scan commands, fuzzing configurations, code-review findings, PoC-oriented analysis, and vulnerability reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow directs users to fetch, build, and run kernel fuzzers, kernel sources, and proof-of-concept oriented artifacts that can affect host stability or expose sensitive systems.

Mitigation: Run fuzzing, kernel builds, and PoCs only inside disposable VMs or isolated lab infrastructure, and avoid privileged accounts or environments containing secrets.

Risk: Downloaded tools and kernel sources introduce supply-chain risk if they are fetched or executed without verification.

Mitigation: Pin or verify downloaded tools and kernel sources before execution.

Risk: Pattern scans and generated findings can produce false positives or misleading vulnerability conclusions.

Mitigation: Manually review scan hits, confirm code context, and validate root cause and exploitability before reporting.

## Reference(s):

- [CVE Pattern Library](references/cve-patterns.md)
- [Subsystem Audit Checklists](references/subsystem-checklists.md)
- [Trinity Fuzzer](https://github.com/kernelsploit/trinity)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, C, YAML, and report-template code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs require expert review before acting on vulnerability findings or executing generated commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
