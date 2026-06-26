## Description: <br>
Half Full is a mindful eating companion for desk workers that tracks meals, profile, weight, and Apple Health-style activity data with a nonjudgmental tone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OakcoderX](https://clawhub.ai/user/OakcoderX) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to log meals, manage body-profile and weight records, parse Apple Health-style activity messages, and generate supportive nutrition summaries for mindful eating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores meal, profile, weight, and Apple Health-style activity records as local plaintext JSON and ships with personal-looking health records. <br>
Mitigation: Review and clear the bundled data files before use, and use the skill only where local plaintext storage of this health-related data is acceptable. <br>
Risk: The security summary flags quiet profiling of sensitive health patterns. <br>
Mitigation: Avoid enabling any menstrual-cycle inference unless the publisher makes it explicit, opt-in, reviewable, and deletable. <br>
Risk: Apple Health-style messages may include steps, calorie burn, and weight data. <br>
Mitigation: Limit synced fields to what is needed, review records before sharing, and delete local records when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OakcoderX/half-full) <br>
- [Publisher profile](https://clawhub.ai/user/OakcoderX) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from local Python scripts plus brief natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores meal, profile, weight, and activity records in local JSON files.] <br>

## Skill Version(s): <br>
0.1.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
