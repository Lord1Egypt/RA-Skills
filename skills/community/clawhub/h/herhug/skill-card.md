## Description: <br>
superSoul provides OpenClaw agents with psychological scoring standards and local user-state data for personality, emotional rhythm, coping, confidence, and response-style guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinqimiao](https://clawhub.ai/user/xinqimiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an OpenClaw assistant maintain confidence-weighted psychological and emotional profiles and tailor response style from those profiles. It is intended for personalized assistant behavior, not clinical diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently builds sensitive psychological and emotional profiles. <br>
Mitigation: Use explicit opt-in, restrict filesystem access to the local profile directory, define retention and deletion procedures, and document who can inspect the stored data. <br>
Risk: Raw message content and inferred traits may be saved locally as part of scoring and profile updates. <br>
Mitigation: Minimize saved content, avoid collecting unnecessary sensitive details, and redact or delete profile records when users request removal. <br>
Risk: Proactive care and intimacy-oriented behavior can be inappropriate in some deployments. <br>
Mitigation: Review or disable proactive follow-up behavior, set clear user expectations, and keep response guidance bounded to non-clinical personalization. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xinqimiao/herhug) <br>
- [Publisher Profile](https://clawhub.ai/user/xinqimiao) <br>
- [README](artifact/README.md) <br>
- [Usage Guide](artifact/USAGE.md) <br>
- [OCEAN and HEXACO Scoring Standard](artifact/standards/01_ocean_hexaco.md) <br>
- [Confidence Scoring Standard](artifact/standards/05_confidence_scoring.md) <br>
- [Attachment Scoring Standard](artifact/standards/07_attachment.md) <br>
- [Interaction Preference Standard](artifact/standards/08_interaction_preference.md) <br>
- [Emotion Trigger Standard](artifact/standards/09_emotion_triggers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown scoring standards and JSON objects for user state, scores, rhythm analysis, confidence reports, follow-up tasks, and response-style guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists per-user local profile data under ~/.openclaw/data/herHug/<userId>/ when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
