## Description: <br>
Megan calculates food calories and provides nutrition-oriented meal guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yamyeed](https://clawhub.ai/user/yamyeed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to estimate calories, calculate TDEE/BMR, plan macros, log meals and hydration, and get nutrition guidance for cycle-aware planning, fasting, blood glucose, digestive health, sleep, stress, and anti-inflammatory diet topics. Users should treat the output as general nutrition guidance, not medical diagnosis or individualized clinical care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal nutrition and body data locally under ~/nutrition-data. <br>
Mitigation: Install only if local storage of this data is acceptable, and review or delete the local JSON files when they are no longer needed. <br>
Risk: Diet, supplement, fasting, pregnancy, PCOS, cycle-related, and blood-glucose guidance could be mistaken for medical care. <br>
Mitigation: Treat outputs as general guidance and consult qualified health professionals for medical conditions, pregnancy, eating disorder history, or other high-risk circumstances. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yamyeed/skills/nutrition-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or plain text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local JSON profile, meal log, hydration, and habit data under ~/nutrition-data.] <br>

## Skill Version(s): <br>
4.2.1 (source: release evidence; artifact frontmatter says 4.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
