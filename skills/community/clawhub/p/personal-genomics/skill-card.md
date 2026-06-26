## Description: <br>
Analyzes raw consumer DNA and VCF files locally to produce health, pharmacogenomics, ancestry, trait, and report outputs for agent-assisted review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wkyleg](https://clawhub.ai/user/wkyleg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to analyze personal genomics files locally and generate prioritized summaries, reports, dashboards, and exports. It is intended for informational interpretation workflows, not clinical diagnosis or treatment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw DNA files and generated health, ancestry, PDF, HTML, and clinical exports contain highly sensitive personal and familial information. <br>
Mitigation: Process files locally, keep outputs out of synced or shared folders, restrict access to generated reports, and delete reports when no longer needed. <br>
Risk: Cancer, medication, APOE, polygenic risk, carrier, and other health outputs may be misread as clinical findings. <br>
Mitigation: Treat results as informational and confirm important findings with qualified medical or genetic professionals before making health decisions. <br>
Risk: The provided security assessment classifies the release as suspicious because of material privacy and medical-interpretation risks. <br>
Mitigation: Install only after reviewing the security guidance and confirming that local processing of raw DNA data is appropriate for the intended environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wkyleg/personal-genomics) <br>
- [Interpretation Guide](references/INTERPRETATION_GUIDE.md) <br>
- [Privacy Guide](references/PRIVACY_GUIDE.md) <br>
- [Security Policy](SECURITY.md) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples, plus generated JSON, text, HTML dashboard, PDF, and clinical export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and writes analysis reports under the configured reports directory.] <br>

## Skill Version(s): <br>
4.2.0 (source: server release and CHANGELOG, released 2026-02-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
