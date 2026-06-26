## Description: <br>
Validate agent nature through SHACL-based heartbeat analysis to classify profiles as Agent, Human, Cron, or Hybrid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darshanochandak](https://clawhub.ai/user/darshanochandak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external ClawHub users use this skill to validate Turtle profile data and classify posting-pattern metrics as Agent, Human, Cron, or Hybrid with SHACL checks and heuristic scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Privacy-sensitive profiling language may encourage overinterpretation of posting-pattern metrics. <br>
Mitigation: Use only authorized profile files, avoid sensitive identifiers in shared logs or terminals, and treat classifications as heuristic rather than identity proof. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darshanochandak/heartbeat-scanner) <br>
- [Heartbeat Scanner README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local analysis of user-supplied Turtle profile files; results are heuristic and non-authoritative.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
