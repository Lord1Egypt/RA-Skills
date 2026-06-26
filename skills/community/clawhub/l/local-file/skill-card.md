## Description: <br>
Reads, summarizes, and searches local text, Markdown, JSON, DOCX, and PDF files within authorized paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhouqing](https://clawhub.ai/user/zhouhouqing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent read, extract, summarize, and search local document contents during workspace tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The file-access boundary is weak for sensitive local files. <br>
Mitigation: Install only for trusted workflows, require explicit user-approved paths, and enforce resolved absolute-path containment before broader use. <br>
Risk: The artifact includes a hardcoded local allowlist path. <br>
Mitigation: Remove or replace the hardcoded path with user- or workspace-configured allowlists. <br>
Risk: The documented 10MB file limit is not enforced by the artifact behavior. <br>
Mitigation: Add an actual file-size check before reading or parsing local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouhouqing/local-file) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown, with structured error messages for unsupported formats or unauthorized paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local text, Markdown, JSON, DOCX, and PDF inputs; file-access controls should be reviewed before broad use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
