## Description:

AI-powered nutrition coach and health tracker powered by Haver for logging food, tracking calories and macros, monitoring weight, receiving AI coaching, and earning XP and achievements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuvasee](https://clawhub.ai/user/yuvasee)

### License/Terms of Use:


## Use Case:

External users use this skill through an agent to onboard with Haver, log meals, review calorie and macro progress, track weight, and receive non-clinical nutrition coaching. The skill is intended for wellness tracking and habit support, not medical nutrition advice or clinical dietetics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive nutrition, weight, profile, image, and coaching chat data that may be sent to and stored by Haver.

Mitigation: Install only when users understand the data flow to Haver, collect the minimum needed data, and keep coaching responses focused on wellness tracking rather than clinical advice.

Risk: The hv_ API key is a personal credential used for authenticated Haver requests.

Mitigation: Treat the API key like a password, avoid exposing it in logs or ordinary conversation memory, and rotate it by re-registering if it may have been exposed.

Risk: The API origin can be configured, and an incorrect origin could send sensitive data to the wrong service.

Mitigation: Verify that HAVER_API_URL is locked to the real Haver service before use.

Risk: Food and profile changes may be stored without an undo or delete path.

Mitigation: Confirm ambiguous food, weight, and profile updates with the user before submitting them, and clearly relay stored results and side-effect messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuvasee/skills/openclaw-nutrition)
- [Haver homepage](https://haver.dev)
- [API Reference](artifact/api-reference.md)
- [Onboarding Guide](artifact/onboarding.md)
- [Coaching & Behavior Guide](artifact/coaching-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration instructions, Guidance]

**Output Format:** [Conversational Markdown with Haver API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate authenticated HTTP API calls to Haver when an agent has the user's hv_ API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
