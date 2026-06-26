## Description: <br>
Skill Manager helps OpenClaw users list installed skills, view skill descriptions, and identify overlapping skill functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[damienCronw](https://clawhub.ai/user/damienCronw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and developers use this skill to inspect locally installed skills, review their descriptions, and spot categories or duplicate capabilities while managing a skill workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented category and duplicate-detection features may not be fully implemented in the current artifact. <br>
Mitigation: Treat category and duplicate findings as informational and verify them against the actual installed skills. <br>
Risk: The script invokes the local clawhub command to list ClawHub-installed skills. <br>
Mitigation: Run it only in an environment where the local clawhub command is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/damienCronw/openclow-skill-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and terminal text listings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local skill inventory; category and duplicate-detection behavior should be treated as informational.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version and artifact metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
