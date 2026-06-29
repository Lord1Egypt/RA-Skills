## Description: <br>
Automatically calibrates mobile FPS game sensitivity from measured angle data and video-based motion analysis, producing physical sensitivity constants and tuning reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanlan987no87](https://clawhub.ai/user/lanlan987no87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players, tool builders, and calibration engineers use this skill to process mobile FPS sensitivity measurements and produce system constants, fit quality, and physical sensitivity metrics for tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's privacy and account-safety wording is overstated for screen recordings. <br>
Mitigation: Keep account, chat, map, and other sensitive details out of recordings when possible, and review recordings before processing or sharing outputs. <br>
Risk: The packaged bridge validates angle input but appears not to pass those values into the core calibration script. <br>
Mitigation: Verify that measured angle data is actually used before relying on calibration results for tuning decisions. <br>
Risk: The skill runs local Python/OpenCV processing on user-provided video files. <br>
Mitigation: Run it only in a trusted local environment and provide only intended gameplay recordings. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanlan987no87/neurosync-calibrator) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact manifest](artifact/manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON results with a raw text calibration report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs K_sys, K_accel, R_squared, sensitivity metrics in degrees per centimeter and degrees per pixel, status, and raw_report.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
