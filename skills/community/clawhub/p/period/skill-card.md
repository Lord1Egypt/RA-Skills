## Description: <br>
Privacy-first menstrual cycle tracking. Auto-learns periods, symptoms, and patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to privately log menstrual cycle starts, symptoms, preferences, and patterns. It helps an agent maintain a local period history and adapt follow-up questions only to information the user explicitly shares. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive period and symptom history may remain on a shared, backed-up, or otherwise accessible device. <br>
Mitigation: Install only where local health data retention is acceptable, and review or delete ~/period/memory.md when sharing the account or device or when the data is no longer wanted. <br>
Risk: Cycle context could be surfaced outside the conversation where the user intended to track it. <br>
Mitigation: Record only cycle information the user explicitly shares, avoid referencing cycle data in unrelated conversations, and support deletion when requested. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/period) <br>
- [Cycle Privacy Guidelines](privacy.md) <br>
- [Cycle Trackable Data](symptoms.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files] <br>
**Output Format:** [Markdown notes and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores sensitive cycle and symptom history locally when the user explicitly shares it.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
