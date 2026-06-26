## Description: <br>
Helps agents turn meeting text into minutes, extract action items, manage local meeting records, and provide meeting templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams, meeting facilitators, and assistant agents use this skill to draft meeting minutes, identify decisions and follow-up tasks, and keep local JSON meeting records for later reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting titles, attendees, notes, and action items can be stored on disk in local JSON files. <br>
Mitigation: Use the skill only where local retention is acceptable, and establish a deletion or retention practice before using it for confidential meetings. <br>
Risk: Reminder and calendar-related behavior is described, but the evidence warns not to rely on it until verified. <br>
Mitigation: Verify reminder and calendar behavior in the target agent environment before depending on it for scheduling workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/meeting-assistant-cp3d) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON files, guidance] <br>
**Output Format:** [Markdown-style responses and local JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores meeting titles, attendees, notes, and action items in local JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
