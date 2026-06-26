## Description: <br>
Track daily calories and macros in Obsidian, with profile initialization (sex/height/weight/goal) and goal-based target checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstract-sum](https://clawhub.ai/user/abstract-sum) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to initialize a nutrition profile, log meals with calorie and macro estimates into an Obsidian vault, and check whether daily intake meets configured targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The profile setup script can run unintended local code if crafted input is passed to it. <br>
Mitigation: Review before installing, use only trusted simple profile values, and prefer a fixed version that passes inputs through environment variables or JSON encoding. <br>
Risk: Nutrition logs and profiles may contain personal health data in the local Obsidian vault. <br>
Mitigation: Keep the vault private and apply local access controls appropriate for health-related records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abstract-sum/nutrition-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/abstract-sum) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes nutrition profile JSON and monthly Obsidian Markdown logs under the configured vault.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
