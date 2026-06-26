## Description: <br>
Harden agent sessions against prompt injection from untrusted content by tagging external text, scanning for attack patterns, guarding memory writes, and documenting canary detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adrianteng](https://clawhub.ai/user/adrianteng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce prompt injection risk when an agent reads web search results, emails, downloaded files, PDFs, API responses, or other untrusted text. It provides practical scanning, tagging, memory-write, and checklist guidance for safer ingestion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local shell and Python helper scripts can wrap commands and write memory or quarantine files, so unintended command use or unreviewed memory entries could affect an agent workspace. <br>
Mitigation: Run the command wrapper only around commands you intended to execute, keep higher-risk integrations read-only where possible, and review quarantine and memory entries periodically. <br>
Risk: Pattern scanning and sanitizer output may miss sophisticated prompt injection or leave instruction-like content in text that appears cleaned. <br>
Mitigation: Do not treat sanitizer output as fully safe instruction-neutral text; re-anchor to the user's original request and require explicit approval before acting on external content. <br>


## Reference(s): <br>
- [Canary Patterns - Prompt Injection Detection](references/canary-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/adrianteng/prompt-injection-defense) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with bash commands and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts can tag untrusted command output, scan text from stdin or files, and append accepted or quarantined memory entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
