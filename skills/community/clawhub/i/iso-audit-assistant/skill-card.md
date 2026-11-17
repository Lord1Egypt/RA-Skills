## Description: <br>
ISO Audit Assistant helps users prepare for ISO management-system certification, surveillance audits, and internal audits by interpreting clauses, parsing documents, analyzing gaps, generating standard-format system documents, converting legacy documents, and running mock-audit Q&A. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kooui](https://clawhub.ai/user/kooui) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external consultants, auditors, and management-system teams use this skill to prepare ISO audit evidence, identify documentation gaps, generate procedure drafts, convert existing documents into audit-ready formats, and rehearse audit responses. Generated materials should be reviewed against the organization's real processes before audit use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded or referenced company documents may contain personal, legal, security, or commercial information. <br>
Mitigation: Redact unnecessary sensitive details and point directory analysis only at folders intended for audit review. <br>
Risk: Generated audit documents, gap analyses, and mock-audit guidance may be incomplete or mismatched to the organization's actual processes. <br>
Mitigation: Have responsible process owners or qualified audit staff review and adapt outputs before using them for certification, surveillance, or internal audits. <br>
Risk: Publisher instructions mention API tokens for release workflows. <br>
Mitigation: Handle tokens as secrets and avoid pasting them into shared terminals, screenshots, logs, or shell history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kooui/skills/iso-audit-assistant) <br>
- [Standard index](artifact/knowledge/standard_index.json) <br>
- [Example interaction](artifact/examples/example_interaction.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated document drafts, gap reports, and JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports bilingual Chinese and English workflows and produces draft audit materials that require human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
