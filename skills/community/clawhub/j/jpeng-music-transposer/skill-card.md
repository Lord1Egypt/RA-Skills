## Description: <br>
Transpose music keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and music workflow users use this skill to transpose music keys and automate transpose tasks from input files to JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced script scripts/music_transposer.py is not included in the artifact for review. <br>
Mitigation: Confirm the script source and review it separately before installation or execution. <br>
Risk: The workflow uses TRANSPOSE_API_KEY and writes to a user-provided output path. <br>
Mitigation: Use a scoped API key only for a known service and review the output path before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-music-transposer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON result shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRANSPOSE_API_KEY for the referenced command-line workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
