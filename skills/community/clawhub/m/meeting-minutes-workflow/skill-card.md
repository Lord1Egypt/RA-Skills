## Description: <br>
Generates structured meeting minutes from discussion notes, optionally syncs them to Feishu docs, and tracks action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams and agents use this skill to turn meeting notes into structured Markdown minutes, optionally sync them to Feishu, and track follow-up action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting notes can contain confidential or personal information and may be sent to Feishu during sync. <br>
Mitigation: Keep output local unless sync is explicitly requested, and confirm the target Feishu document owner, sharing settings, and attendee access before syncing. <br>
Risk: Action items may be saved locally with sensitive names, deadlines, or follow-up details. <br>
Mitigation: Confirm whether action items should be saved, choose an appropriate storage location, and omit sensitive details when local retention is not needed. <br>


## Reference(s): <br>
- [Meeting types reference](references/meeting-types.md) <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/meeting-minutes-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Markdown meeting minutes, JSON action-item records, and optional shell commands for Feishu document creation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Feishu documents when sync is requested and may save action-item records locally for follow-up tracking.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
