## Description: <br>
Immigration process guidance and application organization with strict privacy boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to organize immigration applications: compare general pathways, prepare document checklists, track deadlines and status, and rehearse interview questions while keeping records local. It is for general process support only and does not replace advice from a licensed immigration attorney. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive immigration details may be saved locally in the OpenClaw workspace. <br>
Mitigation: Use the skill only when local storage is acceptable, avoid entering unnecessary sensitive details, and review or delete local memory files when they are no longer needed. <br>
Risk: Visa-specific rights, restrictions, deadlines, and interview guidance may be outdated or too situation-specific. <br>
Mitigation: Verify current requirements with official government sources or a licensed immigration attorney before acting on the guidance. <br>
Risk: The artifact includes process guidance that can exceed the skill's stated boundary against legal advice. <br>
Mitigation: Treat outputs as general organization support and avoid relying on them for legal interpretation or case-specific decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AGIstack/immigration) <br>
- [Pathway Finder](artifact/references/pathway-finder.md) <br>
- [Document Checklist Generator](artifact/references/document-checklist.md) <br>
- [Deadline and Timeline Tracker](artifact/references/deadline-tracker.md) <br>
- [Visa Interview Preparation](artifact/references/interview-prep.md) <br>
- [Application Status Tracking](artifact/references/application-status.md) <br>
- [Post-Approval Planning](artifact/references/post-approval.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command examples and local JSON records created by supporting scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-provided immigration records locally under the OpenClaw workspace when scripts are used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
