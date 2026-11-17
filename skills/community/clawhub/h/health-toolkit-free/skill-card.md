## Description: <br>
A personal health management skill for recording workouts, sleep, diet, health metrics, goals, and basic local trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External personal users use this skill to maintain local health records, track workouts, sleep, diet, metrics, and goals, and generate basic summaries or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store personal health information in local files under ~/.health. <br>
Mitigation: Review file permissions, avoid unintended cloud sync, and consider encryption or separate local storage on shared machines. <br>
Risk: Health summaries and calorie estimates may be incomplete or unsuitable for medical decisions. <br>
Mitigation: Use outputs for personal tracking only and consult qualified professionals for medical, nutrition, or diagnostic decisions. <br>
Risk: Backup or sync commands can copy sensitive health records to additional locations. <br>
Mitigation: Review backup destinations before running commands and confirm that any synced location is intended and access-controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/health-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, configuration examples, and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read local health data files under ~/.health when the agent follows the skill examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
