## Description: <br>
Mbti Guru provides interactive MBTI personality tests in four lengths and generates bilingual personality, career, relationship, and PDF-style reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effeceee](https://clawhub.ai/user/effeceee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to run MBTI-style personality assessments through a CLI or supported messaging channels, resume in-progress tests, and review saved bilingual reports. It is useful for self-assessment, coaching, team-development conversations, and report generation where MBTI-style outputs are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MBTI answers, progress, and results may be stored locally under chat or user identifiers for resume and history features. <br>
Mitigation: Operate the skill with a clear retention policy, limit access to the local data directory, and provide users a way to delete stored session and history data. <br>
Risk: Personality reports can be mistaken for clinical, employment, or high-stakes assessment outputs. <br>
Mitigation: Use the reports as informational self-assessment material and require human review before applying results to consequential decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/effeceee/mbti-guru) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/effeceee) <br>
- [CLAWHUB metadata](artifact/CLAWHUB.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Design document](artifact/DESIGN.md) <br>
- [Report specification](artifact/docs/report_spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Interactive prompts, bilingual text reports, JSON session/history files, and generated PDF report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports 70, 93, 144, and 200-question test versions with local progress and history storage.] <br>

## Skill Version(s): <br>
1.5.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
