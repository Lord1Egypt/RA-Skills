## Description:

Finds and verifies 9-slice borders in game UI panel PNGs, then exports engine-specific nine-patch files for panels it can prove.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT

## Use Case:

Game developers use PatchProof to identify and check nine-patch borders in panel PNGs, then prepare Unity, Godot, or Android assets for panels the tool can verify.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence and partial Skillspector coverage, so it does not establish that the artifact is risk-free.

Mitigation: Review the skill source and install it only if you trust and need it; treat the scanner result as limited evidence.

## Reference(s):

- [PatchProof on ClawHub](https://clawhub.ai/raktikoo/skills/patchproof)
- [PatchProof GitHub installation link](https://github.com/RakTikoo/patchproof)

## Skill Output:

**Output Type(s):** [Analysis, Configuration, Files, JSON]

**Output Format:** [Command-line findings, Unity .meta and Godot .tres configuration, Android .9.png assets, and a JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports are produced only for panels marked PROVEN; uncertain panels are reported without border values or exports.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
