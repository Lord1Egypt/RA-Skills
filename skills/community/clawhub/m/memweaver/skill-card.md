## Description: <br>
Memory Profiler - Mine hidden patterns from your Agent's memory, confirm via interactive quiz, and generate a structured user profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fret774](https://clawhub.ai/user/fret774) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use MemWeaver to analyze local CodeBuddy memory and recent daily logs, ask confirmation questions about inferred patterns, and produce a structured user profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes sensitive personal and work-pattern memory content. <br>
Mitigation: Run it only in trusted local workspaces and use a narrow day range when less context is sufficient. <br>
Risk: Generated YAML profiles and backups may contain sensitive inferences. <br>
Mitigation: Review profile files before sharing or relying on them, and delete generated profiles or backups when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fret774/memweaver) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fret774) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON collection output, interactive questionnaire text, and YAML profile configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Collects local memory content and writes profile_YYYYMMDD.yaml; users can reduce the day range to limit analyzed content.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
