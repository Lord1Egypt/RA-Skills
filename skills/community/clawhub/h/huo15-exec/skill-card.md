## Description: <br>
Guides an agent to verify code changes with targeted commands, tests, builds, and honest result reporting while treating destructive operations cautiously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use this skill after code changes to choose focused verification commands, reproduce bugs when relevant, rerun failed checks after fixes, and report results and gaps clearly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification guidance can lead an agent to propose destructive or production-affecting commands. <br>
Mitigation: Review and explicitly approve destructive, irreversible, privileged, or production-affecting commands before execution. <br>
Risk: Passing a narrow check can create false confidence if relevant tests, builds, or failure cases were skipped. <br>
Mitigation: Require the agent to report which commands ran, their outcomes, and any important coverage gaps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-exec) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external tools or binaries are required by the skill metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
