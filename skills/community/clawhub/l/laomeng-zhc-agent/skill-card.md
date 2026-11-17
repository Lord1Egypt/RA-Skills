## Description:

Helps agents integrate the ZHC Chinese programming language into editors and runtimes, run compile, execution, diagnosis, and Office-export workflows, and maintain compatibility with its documented contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxh678988](https://clawhub.ai/user/mxh678988)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to connect ZHC language services to editors and automation runtimes, compile and diagnose Chinese-language programs, and run Office or web export workflows. It also provides checks for maintaining compatibility with ZHC's documented contracts and release baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan classifies this release as suspicious; its inspection was incomplete and reports concerns involving execution, input handling, and availability.

Mitigation: Review the security findings before installation, and do not rely on the reported passive inspection mode for untrusted WebAssembly.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mxh678988/skills/laomeng-zhc-agent)
- [Publisher profile](https://clawhub.ai/user/mxh678988)
- [ZHC agent workflow](artifact/references/智能体工作流.md)
- [LSP protocol](artifact/references/LSP协议.md)
- [Bridge message protocol](artifact/references/桥报文协议.md)
- [ZHC 1.8 contract reference](artifact/references/契约_1.8_全量参考.md)
- [Quick reference](artifact/references/快速参考.md)
- [Error code reference](artifact/references/错误码表_E_1.5.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflows can report diagnostics and export status, including a CSV fallback when an Office bridge is unavailable.]

## Skill Version(s):

1.0.15 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
