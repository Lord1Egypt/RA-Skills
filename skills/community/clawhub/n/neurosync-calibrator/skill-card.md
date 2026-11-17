## Description:

Calibrates mobile FPS game sensitivity from 12 measured rotation angles and video-derived gesture trajectories, returning tuning constants and physical sensitivity metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanlan987no87](https://clawhub.ai/user/lanlan987no87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and FPS players can use this skill to estimate game sensitivity constants and touch movement metrics from measured mobile gameplay calibration data. The output should be reviewed before use because the security evidence reports that calibration results may not reflect submitted measurements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calibration output may not reflect the user's submitted angle measurements.

Mitigation: Do not rely on results until submitted angles are passed into the core calculation and fixed fallback constants are removed.

Risk: Privacy masking claims are overconfident and masking limits are not documented.

Mitigation: Document the masking scope and avoid processing sensitive gameplay video until masking behavior has been verified.

Risk: Runtime hardening is incomplete for dependencies and child script execution.

Mitigation: Pin dependency versions and resolve child scripts from the trusted package directory before deployment.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Artifact manifest](artifact/manifest.json)
- [ClawHub skill page](https://clawhub.ai/lanlan987no87/skills/neurosync-calibrator)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object with numeric calibration fields and a raw text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires exactly 12 measured angle values as input; returns status and calibration metrics such as K_sys, K_accel, R_squared, deg_per_cm_slow, deg_per_cm_fast, and granular_res_deg_per_px.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
