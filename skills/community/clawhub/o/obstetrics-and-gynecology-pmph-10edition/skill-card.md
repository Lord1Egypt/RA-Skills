## Description: <br>
Provides a registry of 187 obstetrics and gynecology reference workflows based on PMPH Obstetrics and Gynecology, 10th edition, covering pregnancy, delivery, high-risk obstetrics, gynecologic oncology, infertility, infections, procedures, and education. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xllgreen](https://clawhub.ai/user/xllgreen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Qualified obstetrics and gynecology clinicians, reproductive medicine professionals, and supervised medical education users can use this skill to retrieve structured reference guidance across topic-specific workflows. It should not be used as standalone medical advice, prescribing guidance, emergency care instruction, or procedural training. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-risk clinical treatment, procedure, and dosing guidance may be inappropriate for general installation or unsupervised use. <br>
Mitigation: Install only for qualified obstetrics and gynecology, oncology, reproductive medicine, or supervised medical education contexts, and require clinician review before acting on outputs. <br>
Risk: Guidance may conflict with current local guidelines, institutional protocols, or patient-specific contraindications. <br>
Mitigation: Verify regimens, procedures, thresholds, and follow-up plans against current local standards and institutional policy before use. <br>
Risk: Emergency, invasive procedure, chemotherapy, pregnancy termination, and sensitive sexual-health topics can create patient-safety or privacy harm if handled casually. <br>
Mitigation: Add explicit warnings for these scenarios, route urgent cases to emergency care, and restrict access to users with an appropriate clinical or supervised educational need. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xllgreen/obstetrics-and-gynecology-pmph-10edition) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill registry](artifact/SKILL.md) <br>
- [Skill index](artifact/index.md) <br>
- [Chemotherapy dosing reference](artifact/ovarian-cancer-chemotherapy-regimen-selection/references/chemotherapy-dosing.md) <br>
- [Preeclampsia blood-pressure and auxiliary-exam reference](artifact/preeclampsia-diagnosis-severe-features/references/血压测量与辅助检查规范.md) <br>
- [Cervical cancer screening protocols reference](artifact/cervical-cancer-three-tier-prevention-strategy/references/screening-protocols-detailed.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reference guidance with occasional shell commands and generated Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundle includes shell scripts for keyword search and report generation; clinical outputs require qualified review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
