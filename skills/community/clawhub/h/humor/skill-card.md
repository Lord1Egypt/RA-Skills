## Description: <br>
Develop adaptive humor that learns what makes each user laugh through signal detection, graduated testing, and graceful failure recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to decide when humor is appropriate, calibrate humor style from user signals, and recover gracefully when a joke does not land. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may keep local notes about humor preferences and interaction history under ~/humor/. <br>
Mitigation: Review or delete ~/humor/ to inspect or reset saved humor history, callbacks, and inferred preferences. <br>
Risk: Humor can be inappropriate in stressed, task-focused, professional, or external communication contexts. <br>
Mitigation: Follow the skill's default zero-humor posture for serious contexts and only increase humor after clear positive signals. <br>


## Reference(s): <br>
- [Humor Skill Page](https://clawhub.ai/ivangdavila/humor) <br>
- [Context-Aware Humor](artifact/contexts.md) <br>
- [Feedback System](artifact/feedback.md) <br>
- [Signal Detection](artifact/signals.md) <br>
- [Humor Types](artifact/types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance and local preference notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain a local humor profile under ~/humor/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
