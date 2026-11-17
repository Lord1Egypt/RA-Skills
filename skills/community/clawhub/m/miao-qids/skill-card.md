## Description:

Analyzes PCAP traffic with a classic–quantum intrusion detector, reporting traffic classifications, confidence scores, conversation details, and security suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsherryyann](https://clawhub.ai/user/tsherryyann)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and developers use this skill to inspect PCAP captures, investigate suspected attacks such as WebShell activity, and interpret network conversation patterns and detection confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public IPs observed in sensitive PCAPs are sent to an external geolocation service by default.

Mitigation: Use --no-ip-query for sensitive captures unless sharing those IPs is acceptable.

Risk: Downloaded model files can execute unsafe code when loaded.

Mitigation: Only load model files from a trusted, verified source.

Risk: Exposing the analysis server could allow unwanted access to local PCAP analysis.

Mitigation: Keep the HTTP service bound to localhost.

Risk: The skill includes an embedded quantum-cloud token.

Mitigation: The publisher should remove and rotate the token before deployment.

## Reference(s):

- [MiaoQIDS on ClawHub](https://clawhub.ai/tsherryyann/skills/miao-qids)
- [MiaoQIDS skill homepage](https://www.skillhub.cn/skills/user_263cfa82/miao-qids)
- [Quantum model download referenced by skill](https://gitee.com/TSherry/MiaoQIDS/releases/download/0.2.0/qnn_model.pkl)
- [Classic model download referenced by skill](https://gitee.com/TSherry/MiaoQIDS/releases/download/0.2.0/cnn_mtd_final.pth)
- [Feature model archive referenced by skill](https://gitee.com/TSherry/MiaoQIDS/releases/download/0.2.0/特征选择结果.zip)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [JSON analysis results and human-readable security recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes traffic-class confidence scores, IP analysis, and PCAP conversation summaries; model-based analysis requires separately obtained model files.]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
