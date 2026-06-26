## Description: <br>
Automatically manages OpenClaw memory tiers, including working memory, short-term memory, long-term memory, memory merging, compression, cleanup, and archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyblhl](https://clawhub.ai/user/wyblhl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to organize local memory files into working, short-term, and long-term tiers, prune older learning and conversation records, and generate memory reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move and delete local OpenClaw memory files without an interactive confirmation step. <br>
Mitigation: Back up the OpenClaw memory directory before use, review the hard-coded paths and retention limits, and run it only in a workspace where automatic cleanup is acceptable. <br>
Risk: The script targets hard-coded Windows paths under D:\OpenClaw\workspace. <br>
Mitigation: Confirm those paths match the intended environment or adjust them before executing the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wyblhl/memory-manager-wyblhl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create logs, JSON reports, archived memory files, and tiered memory directories when its script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
