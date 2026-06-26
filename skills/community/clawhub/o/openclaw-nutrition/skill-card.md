## Description: <br>
Nutrition tracking is an AI-powered nutrition coach and health tracker powered by Haver for logging food, tracking calories and macros, monitoring weight, and getting coaching feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yuvasee](https://clawhub.ai/user/Yuvasee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to log meals in natural language, review calorie and macro progress, track weight, complete onboarding, and receive nonjudgmental nutrition coaching through Haver. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends and stores sensitive diet, weight, profile, and optional image data with Haver. <br>
Mitigation: Install only if the user is comfortable using Haver for nutrition and weight tracking, and avoid sending photos or health details they do not want stored. <br>
Risk: The personal hv_ API key grants access to the user's Haver account data. <br>
Mitigation: Treat the API key like a password, save it only in appropriate persistent memory, and re-register to rotate it if it is lost or exposed. <br>
Risk: Food mentions can be ambiguous and may be logged when the user only intended to discuss food. <br>
Mitigation: Be explicit when a food mention is discussion rather than a log entry, and confirm ambiguous intent before calling food logging endpoints. <br>
Risk: Nutrition coaching may be mistaken for medical nutrition or clinical dietetics advice. <br>
Mitigation: Use the skill for tracking and general coaching, not clinical advice, and direct medical nutrition questions to qualified professionals. <br>


## Reference(s): <br>
- [Haver homepage](https://haver.dev) <br>
- [ClawHub release page](https://clawhub.ai/Yuvasee/openclaw-nutrition) <br>
- [API reference](artifact/api-reference.md) <br>
- [Onboarding guide](artifact/onboarding.md) <br>
- [Coaching guide](artifact/coaching-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Conversational text and markdown with HTTP API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Haver API responses for nutrition summaries, weight tracking, onboarding status, rewards, and coaching context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
