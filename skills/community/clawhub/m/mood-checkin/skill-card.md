## Description: <br>
Mood Checkin provides a Sol persona for short mood check-ins, emotional weather reports, guided breathing, journaling, venting, recaps, read-me reflections, archetypes, and monthly summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharoonsharif](https://clawhub.ai/user/sharoonsharif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run personal emotional check-ins, capture short reflections, generate shareable mood summaries, and receive lightweight grounding prompts. The skill is a self-awareness companion, not a therapist, counselor, or medical professional. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses sensitive emotional check-ins, inferred patterns, archetypes, and monthly summaries in a local mood-checkin-profile.json file. <br>
Mitigation: Use it in a private workspace, avoid sharing generated cards unless intentional, and delete mood-checkin-profile.json when resetting or removing stored history. <br>
Risk: The skill discusses emotional distress and may encounter crisis language while explicitly not acting as a therapist or medical professional. <br>
Mitigation: Preserve the skill's disclaimer, avoid clinical claims, and route crisis situations to real human support such as 988 or the listed crisis resources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sharoonsharif/mood-checkin) <br>
- [International Association for Suicide Prevention Crisis Centres](https://www.iasp.info/resources/Crisis_Centres/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Conversational text and markdown-style shareable cards, with a local JSON mood profile when persistence is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains mood-checkin-profile.json with mood history, streaks, archetypes, and monthly summaries.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
