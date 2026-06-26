## Description: <br>
Batch extraction of experimental methods from multiple papers for protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and evidence-review teams use this skill to extract and compare experimental protocol details across multiple research papers, with explicit assumptions and fallback handling when inputs are incomplete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper performs local methodology comparison and may produce incomplete or misleading protocol summaries when source papers are incomplete, inconsistently formatted, or outside the documented scope. <br>
Mitigation: Confirm the input papers, scope filters, method type, output expectations, and assumptions before execution; review the resulting comparison before relying on it. <br>
Risk: The skill is intended for local paper files and workspace outputs, so uncontrolled paths or untrusted files can create operational risk. <br>
Mitigation: Run it only against paper files in a workspace you control and keep generated outputs within the workspace. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/methodology-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON-style comparison outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should separate assumptions, workflow, deliverables, risks, unresolved items, and validation checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
