## Description: <br>
Provides daily Islamic reflections with Hijri calendar awareness, Quran and Hadith references, and practical daily challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clinicode](https://clawhub.ai/user/clinicode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users ask an agent for an Islamic daily reflection or reminder. The skill runs a local Python script that selects a calendar-aware reflection and returns formatted spiritual guidance with a practical action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts api.aladhan.com to look up the Hijri date, which depends on that service and may reveal basic request metadata. <br>
Mitigation: Use the skill only where that external date lookup is acceptable, and avoid sensitive prompts when external request metadata should not be exposed. <br>
Risk: Broad prompts such as "inspire me" may trigger Islamic religious reflection when the user intended non-religious inspiration. <br>
Mitigation: Invoke the skill for explicitly Islamic reminders or reflections, and choose a different skill for general motivational content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clinicode/islamic-daily-reflection) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Formatted plain text produced by a Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output includes date context, a reflection, an action item, and a Quran or Hadith reference.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
