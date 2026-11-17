## Description:

Analyzes 3D mesh files (STL) to calculate geometric properties (volume, components) and extract attribute data. Use this skill to process noisy 3D scan data and filter debris.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze STL mesh files, estimate component volume, isolate the largest connected component from noisy scans, and read material or color identifiers stored in binary STL attribute bytes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Very large or adversarial STL files may make local mesh analysis slow or memory-heavy.

Mitigation: Run analysis on expected local STL files and apply external file-size or runtime limits before processing untrusted inputs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [Markdown with Python examples and dictionary-shaped analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces volume, material ID, and component-count values; volume uses the STL coordinate units cubed.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
