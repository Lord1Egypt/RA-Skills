## Description: <br>
Track source-of-truth relationships between files and identify when derived content becomes stale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and maintainers use Golden Master to map source files to derived documentation, establish checksum metadata, and validate when derived content needs review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads repository files to compare source and derived documentation. <br>
Mitigation: Use it in trusted workspaces and avoid applying it to files that should not be processed by the configured agent model. <br>
Risk: Suggested relationships may reflect coincidental similarity, and checksum freshness does not prove semantic correctness. <br>
Mitigation: Confirm source and derived relationships, then review source changes before relying on staleness reports or refreshing metadata. <br>
Risk: Generated checksum metadata comments or shell command examples could be copied into files incorrectly. <br>
Mitigation: Review generated comments and commands before use, and modify files only after explicit user approval. <br>


## Reference(s): <br>
- [Golden Master homepage](https://github.com/live-neon/skills/tree/main/pbd/golden-master) <br>
- [Golden Master on ClawHub](https://clawhub.ai/leegitw/golden-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples, metadata comments, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces suggested relationships, staleness reports, and checksum metadata for user review; does not auto-modify files without explicit request.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
