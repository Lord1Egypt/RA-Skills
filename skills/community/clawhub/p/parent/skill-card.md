## Description: <br>
Parent.skill is a shared parenting co-pilot that helps caregivers track feeding, sleep, milestones, soothing methods, and daily routines from their own observations without providing medical advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers use this skill to maintain a shared local record of a child's feeding, sleep, soothing patterns, milestones, and recent activity. It supports logging, quick routine queries, and caregiver briefings while directing medical concerns to a pediatrician. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive details about a child and family routine in local files. <br>
Mitigation: Install and use it only where authorized caregivers can access the local ~/.parent-skill/children/ folder, and protect or delete that folder when access should change. <br>
Risk: Caregiver prompts or logs could include unnecessary medical or identifying details. <br>
Mitigation: Ask for and record only the observations needed for the routine, and avoid extra medical or identifying information unless the caregiver intentionally provides it. <br>
Risk: Routine pattern summaries could be mistaken for medical guidance. <br>
Mitigation: Keep responses framed as observations from the caregiver's data and direct illness, fever, rash, or other health concerns to a pediatrician. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/realteamprinz/parent) <br>
- [Developmental Stages Reference](references/developmental-stages.md) <br>
- [Baby Profile Template](templates/BABY-PROFILE.md) <br>
- [Daily Log Format](templates/DAILY-LOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown responses plus local Markdown and JSONL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores child observations locally under ~/.parent-skill/children/ when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
