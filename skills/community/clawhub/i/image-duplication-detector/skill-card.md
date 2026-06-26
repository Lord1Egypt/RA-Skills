## Description: <br>
Detects image duplication and possible tampering in manuscript figures using computer vision algorithms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, editors, and publication integrity reviewers use this skill to scan manuscript PDFs or image folders for repeated figures and possible local tampering. It supports manual review by producing similarity and suspicious-region reports; it does not determine misconduct on its own. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency hygiene issues can make installation unreliable or pull unintended packages. <br>
Mitigation: Install in an isolated virtual environment and replace requirements.txt with pinned canonical packages such as opencv-python and Pillow before relying on the tool. <br>
Risk: Manuscripts, extracted page images, and generated reports may contain confidential publication data. <br>
Mitigation: Use dedicated output and temporary directories, keep processing local, and delete generated reports or extracted page images when they are no longer needed. <br>
Risk: Similarity and tampering signals can produce false positives or miss subtle edits. <br>
Mitigation: Treat results as review cues and have a qualified reviewer inspect the source figures before making publication-integrity decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/image-duplication-detector) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Files] <br>
**Output Format:** [JSON report with optional PNG visualization file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include summary counts, duplicate groups, similarity scores, and suspicious tampering regions when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
