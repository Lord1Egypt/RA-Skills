## Description:

Analyzes a code workspace and reports total files, total lines, and language distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[douduandou](https://clawhub.ai/user/douduandou)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to estimate project size, code volume, language mix, and changes in codebase complexity over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recursive scanner can follow symlinks outside the intended workspace and read more files than expected.

Mitigation: Review before installation, run only against an intended workspace, and prefer a version that rejects or safely handles symlinks and enforces workspace containment.

Risk: Large workspaces or linked directories can make scans slow or resource-intensive.

Mitigation: Prefer a version with configurable repository paths, file limits, and depth limits before using it in large workspaces.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text console summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports total file count, total line count, and per-language file, line, and percentage totals.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
