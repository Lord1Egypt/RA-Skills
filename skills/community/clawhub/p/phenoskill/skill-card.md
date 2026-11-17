## Description:

Extract clinical phenotypes and medication entities from user-provided text using PhenoSnap, producing a timestamped JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaichop](https://clawhub.ai/user/kaichop)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to extract phenotype and medication entities from clinical free text they provide, while keeping processing local and writing timestamped JSON artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download and run mutable third-party PhenoSnap code and install Python packages during setup.

Mitigation: Run it in a dedicated virtual environment or container, prefer a pinned and reviewed PhenoSnap release, and verify dependency hashes before use.

Risk: The skill processes sensitive clinical text and writes redacted inputs and JSON outputs to local files.

Mitigation: Remove identifiable clinical information before use, keep file access limited to the working directory, and avoid using identifiable clinical records unless local handling is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaichop/skills/phenoskill)
- [PhenoSnap upstream repository](https://github.com/WGLab/PhenoSnap.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown response with file paths and timestamped JSON output artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, an HPO OBO file via HPO_OBO_PATH or resources/hp.obo, and first-run network access when PhenoSnap is not already cached.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
