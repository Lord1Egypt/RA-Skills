## Description: <br>
Autonomous behavioral research loop that optimizes agent behavior through correction tracking and multi-perspective (MAGI) verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teenu](https://clawhub.ai/user/teenu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep local correction notes and measured behavior rules so an agent can adapt to repeated user preferences with review checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps local correction and preference notes that may steer future behavior in unwanted ways. <br>
Mitigation: Periodically review or clear memory.md, corrections.md, and experiments.md, and use the documented forget flow for unwanted rules. <br>
Risk: Autonomous behavior tuning may reduce review interruptions and allow an unwanted preference to persist longer. <br>
Mitigation: Keep autonomous mode off unless deliberately enabling less-interrupted tuning, and review applied rules before they become persistent. <br>
Risk: A self-evaluating loop can mistake the absence of correction for success and drift from user intent. <br>
Mitigation: Require explicit correction evidence, ask when signals are ambiguous, and surface rule sets for review after repeated failures or long success streaks. <br>
Risk: Correction logs could accidentally include sensitive information. <br>
Mitigation: Do not store credentials, financial data, health information, or third-party information in the skill's local memory files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teenu/magi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown notes and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates local memory.md and appends correction and experiment logs when active.] <br>

## Skill Version(s): <br>
1.8.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
