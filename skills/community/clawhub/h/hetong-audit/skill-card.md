## Description:

AI合同审核工具 - 规则引擎 + AI语义分析 + 民法典背书，签合同前先瞄一眼。

This skill is ready for commercial/non-commercial use.

## Publisher:

[moan19921019-code](https://clawhub.ai/user/moan19921019-code)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to review pasted or uploaded Chinese contract text before signing, identify missing clauses and semantic risk areas, and receive a structured risk report with suggested revisions. The results are legal-assistance guidance and should be reviewed by a qualified lawyer for important agreements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided contracts may contain confidential business, personal, or sensitive legal terms.

Mitigation: Redact sensitive content where possible, confirm before processing uploaded contracts, and delete contract_audit_report.html when local retention is not desired.

Risk: Contract review output may be mistaken for formal legal advice.

Mitigation: Treat findings as legal-assistance guidance and consult a qualified lawyer before signing important contracts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moan19921019-code/skills/hetong-audit)
- [Server-resolved GitHub Source](https://github.com/moan19921019-code/hetong-audit)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, code, files, guidance]

**Output Format:** [HTML report saved as contract_audit_report.html, with a short conversational summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts pasted contract text or text extracted from .docx and .pdf files; image-only contracts require a text version.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
