## Description: <br>
Track daily caloric intake by sending food photos. Luna analyzes images using vision AI, estimates calories and macros, and stores everything in memory for daily/weekly summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sidneyschwartz](https://clawhub.ai/user/sidneyschwartz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users use this skill to log meals from food photos, estimate nutrition, and retrieve daily or weekly calorie summaries from agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meal photos and nutrition history may contain sensitive personal information. <br>
Mitigation: Install only when the configured vision model and memory storage are appropriate for the user's privacy needs; delete stored food history or goals when they should no longer persist. <br>
Risk: Food-photo calorie and macro estimates can be inaccurate. <br>
Mitigation: Treat generated nutrition values as estimates, provide portion-size details when possible, and avoid relying on the skill as medical or dietetic advice. <br>


## Reference(s): <br>
- [Luna Calorie Tracker on ClawHub](https://clawhub.ai/sidneyschwartz/luna-calorie-tracker) <br>
- [sidneyschwartz Publisher Profile](https://clawhub.ai/user/sidneyschwartz) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with nutrition summaries, memory file entries, slash-command results, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a vision-capable model and OPENAI_API_KEY or an equivalent provider credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
