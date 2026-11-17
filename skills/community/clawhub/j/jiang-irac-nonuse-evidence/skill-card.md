## Description:

CNIPA撤三（连续三年不使用）双轨证据引擎：答辩证据链构建 + 质证审计（SJ-6 + IRAC + 风险A-E）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisngzhongling](https://clawhub.ai/user/jisngzhongling)

### License/Terms of Use:

Commercial License

## Use Case:

Trademark and IP professionals use this skill to organize evidence, generate defense or cross-examination materials, and review risk for China trademark non-use cancellation matters. It provides technical and methodological support and does not replace legal review.

### Deployment Geography for Use:

China (CNIPA trademark non-use proceedings)

## Known Risks and Mitigations:

Risk: The local WebUI can expose sensitive case data and logs if made reachable from a network-accessible host or used before read endpoints require authentication.

Mitigation: Keep the WebUI bound to 127.0.0.1 and avoid network-accessible hosts until read endpoints enforce authentication.

Risk: The skill writes case material, OCR cache, generated documents, diagnostic JSON, and logs to disk.

Mitigation: Use a private output directory that is not unintentionally shared, synced, or reused across unrelated matters.

Risk: Unpinned dependencies can make production installs less reproducible.

Mitigation: Pin and review dependencies before production deployment when reproducible installs are required.

Risk: Generated legal documents and risk assessments may be incomplete or unsuitable for a specific filing.

Mitigation: Have a qualified professional review the evidence mapping, generated documents, and submission decision before filing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisngzhongling/skills/jiang-irac-nonuse-evidence)
- [README](artifact/README.md)
- [Installation and run guide](artifact/INSTALL.md)
- [Legal disclaimer](artifact/DISCLAIMER.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance plus generated DOCX/PDF/TXT/HTML case files and JSON audit artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes case outputs, OCR cache, logs, rule profiles, reason chains, and validation JSON files to a user-selected local output directory.]

## Skill Version(s):

3.0.1 (source: server release metadata and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
