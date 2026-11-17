## Description:

Unified parenting co-pilot for both parents. Track your baby's patterns together — feeding, sleep, milestones, soothing playbook. One source of truth for mom, dad, grandparents, and caregivers. Self-learning. Not medical advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External caregivers use this skill to keep a shared local record of a baby's feeding, sleep, milestones, soothing results, and daily activity. It supports quick logging, caregiver handoffs, and routine-focused summaries without providing medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive baby and caregiver observations are stored as readable local files.

Mitigation: Use only on trusted devices, protect account and backup access, and delete ~/.parent-skill/children/ when the records should no longer be retained.

Risk: Routine and pattern guidance could be mistaken for medical advice.

Mitigation: Keep the skill's not-medical-advice boundary visible and consult a pediatrician for illness, fever, or health concerns.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/realteamprinz/skills/parent)
- [Developmental Stages Reference](references/developmental-stages.md)
- [Baby Profile Template](templates/BABY-PROFILE.md)
- [Daily Log Template](templates/DAILY-LOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Concise text responses, Markdown profile/playbook content, and JSONL-style daily log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides the agent to maintain local plain-text family records under ~/.parent-skill/children/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
