## Description: <br>
Use when diagnosing KWDB incidents from logs, metrics, or system evidence, especially crashes, OOM, slow SQL, restarts, and cluster-wide availability symptoms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kwdb](https://clawhub.ai/user/kwdb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DBAs, and support engineers use this skill to diagnose KWDB crashes, OOM events, restarts, slow SQL, and cluster availability incidents from logs, metrics, system evidence, and optional source code. It produces Chinese-language diagnostic conclusions while keeping recovery planning, repair sequencing, and reproduction plans out of scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask to inspect or download a KWDB source repository for source-level localization. <br>
Mitigation: Confirm the exact source first, prefer a trusted local checkout, and avoid executing downloaded code automatically. <br>
Risk: The skill is designed to answer in Chinese, which may not fit every review or operations workflow. <br>
Mitigation: Install it only where Chinese-language diagnostics are acceptable or override the language requirement before use. <br>
Risk: Insufficient logs, metrics, system evidence, or source access can lead to partial diagnostic conclusions. <br>
Mitigation: Use the intake gate to collect the fault time, evidence roots, path-specific inputs, and source access status before deep diagnosis. <br>


## Reference(s): <br>
- [Key Rules](references/key-rules.md) <br>
- [Intake Gate](references/intake-gate.md) <br>
- [Path Discovery](references/path-discovery.md) <br>
- [Triage Playbook](references/triage-playbook.md) <br>
- [Fault Localization Chain](references/fault-localization.md) <br>
- [Evidence Rules](references/evidence-rules.md) <br>
- [Output Modes](references/output-modes.md) <br>
- [KWDB Source Repository](https://gitee.com/kwdb/kwdb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown diagnostic report, with command snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Diagnosis-only output; defaults to a general diagnostic report and uses a seven-section test-case template only when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: target metadata and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
