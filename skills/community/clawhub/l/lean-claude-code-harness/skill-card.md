## Description: <br>
Use when building, auditing, or simplifying an AI coding-agent harness, especially when the current runtime has unclear config precedence, weak tool permissions, hidden product-only behavior, or poor transcriptability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aznikline](https://clawhub.ai/user/aznikline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, audit, or simplify Claude Code-style coding-agent harnesses. It focuses the review on explicit configuration precedence, permission-aware tool execution, file-backed skill discovery, transcript persistence, and a traceable query loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Harness recommendations can affect permission checks, configuration precedence, or generated code in a coding-agent runtime. <br>
Mitigation: Review and test any harness changes before deployment, including config precedence, permission filtering, skill discovery, transcript persistence, and the query loop. <br>
Risk: Transcript persistence may store sensitive user or project data. <br>
Mitigation: Define transcript access controls, retention, and redaction expectations before enabling persistent session storage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aznikline/lean-claude-code-harness) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with checklists and implementation review points] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no scripts, installs, credentials, or hidden data access are present in the release evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
