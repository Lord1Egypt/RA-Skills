## Description: <br>
Professional beautification tool for gene expression heatmaps, automatically adds clustering trees, color annotation tracks, and intelligently optimizes label layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and data-analysis agents use this skill to generate publication-ready gene expression heatmaps from CSV expression matrices, with clustering, annotation tracks, label layout optimization, and optional metadata export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CSV expression matrices and annotation JSON files may contain sensitive research data. <br>
Mitigation: Use only files intended to be shared with the agent, and run the skill in an isolated Python environment. <br>
Risk: Unpinned plotting and data dependencies can change rendering or behavior over time. <br>
Mitigation: Use pinned or reviewed dependency versions before production or publication workflows. <br>
Risk: Large matrices can take longer to process and may produce dense labels that need review. <br>
Mitigation: Test with demo mode or a representative subset, adjust figure size and DPI, and review generated figures before publication. <br>
Risk: Audit evidence notes that documented error-handling improvements should be verified against the script. <br>
Mitigation: Run the documented quick checks, demo mode, and missing-file failure path in the target environment before deployment. <br>


## Reference(s): <br>
- [Heatmap Beautifier on ClawHub](https://clawhub.ai/AIPOCH-AI/heatmap-beautifier) <br>
- [Skill README](artifact/SKILL.md) <br>
- [Audit Result](artifact/heatmap-beautifier_audit_result_v2.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown responses with Python or shell examples; generated heatmap files in PDF, PNG, or SVG and optional JSON metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local CSV expression matrices and optional JSON annotation files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
