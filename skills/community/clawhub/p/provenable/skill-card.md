## Description: <br>
Documentation-only skill for using AEGX Provenable as a runtime guide for agent guardrails, verification, CLI workflows, integration, packaging, and incident-response evidence handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, integrators, operators, and incident investigators use this skill to understand, operate, package, or adapt AEGX Provenable workflows. It summarizes how to build or install the runtime, initialize state, check daemon health, run self-verification, create snapshots, and export or verify evidence bundles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes an external runtime, daemon, installer, and binaries that are not bundled with the documentation-only release. <br>
Mitigation: Obtain external software from a trusted source and verify integrity before installation or execution. <br>
Risk: The referenced runtime may monitor agent activity or require elevated access depending on deployment. <br>
Mitigation: Review its monitoring, persistence, daemon health, and permission behavior before granting elevated access. <br>
Risk: A degraded or unreachable guard runtime can give a false sense of protection during risky operations. <br>
Mitigation: Check daemon status and active self-verification before high-impact actions, and pause risky work when coverage is stale or uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielfoojunwei/provenable) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/danielfoojunwei) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command examples and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable code or hidden install behavior is bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
