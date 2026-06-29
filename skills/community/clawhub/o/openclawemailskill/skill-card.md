## Description: <br>
Use when Codex, Hermes, OpenClaw, Claude Code, Cowork, or another AI agent needs to plan, review, implement, audit, or improve email work focused on open, inspectable email campaign operations for agents that need clear audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and authorized staff use this skill to plan, audit, migrate, QA, and prepare approval-gated email campaign operations with clear evidence trails and rollback notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Official correspondence or live email changes may be sent or applied without proper case and recipient review. <br>
Mitigation: Install only for authorized staff and require human verification of the case, recipient, subject, body, and explicit approval before high-risk actions. <br>
Risk: Provider migrations or production email operations can lose suppression, audience, template, or automation parity. <br>
Mitigation: Use provider-neutral checklists, compare source and target capabilities, document rollback notes, and keep high-risk operations behind approval gates. <br>


## Reference(s): <br>
- [OpenClaw Email Skill Operating Checklist](artifact/references/operating-checklist.md) <br>
- [OpenClaw Email Skill ClawHub Release](https://clawhub.ai/polnikale/openclawemailskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with audit trails, playbooks, checklists, review packets, and runbooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates evidence from recommendations and requires explicit approval before live sends, imports, DNS changes, suppression edits, or production automation changes.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
