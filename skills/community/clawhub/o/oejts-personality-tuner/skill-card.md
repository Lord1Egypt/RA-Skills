## Description: <br>
Administer and score the Open Extended Jungian Type Scales (OEJTS 1.2), map results to MBTI-style interaction preferences, and propose/apply personality-aware tuning updates to USER.md and SOUL.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[salvagedeck](https://clawhub.ai/user/salvagedeck) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to run an OEJTS questionnaire, calculate an MBTI-style preference profile, and tune assistant behavior through reviewed USER.md and SOUL.md updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questionnaire-derived interaction preferences can persist in USER.md and SOUL.md. <br>
Mitigation: Run the dry-run first, review the managed blocks, and remove those blocks later if the personalization is no longer wanted. <br>
Risk: Personality results may be overread as fixed identity rather than preference signals. <br>
Mitigation: Treat OEJTS output as adjustable guidance and let explicit user feedback override the profile. <br>


## Reference(s): <br>
- [OEJTS 1.2 Reference](references/oejts-1.2.md) <br>
- [Behavior Mapping](references/behavior-mapping.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/salvagedeck/oejts-personality-tuner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown questionnaire output, JSON scoring output, and managed Markdown blocks for USER.md and SOUL.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode to preview managed workspace-file updates before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
