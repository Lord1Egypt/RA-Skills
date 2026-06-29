## Description: <br>
Applies stewardship virtues such as Care, Curiosity, Humility, Diligence, and Foresight to plugin work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill while authoring plugins, reviewing code quality, improving contributor experience, and reflecting at workflow boundaries such as commits or pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect a broad set of repository documentation and agent-instruction files. <br>
Mitigation: Use it only in repositories where that review scope is acceptable, and keep sensitive material out of prompts and documentation shared with the agent. <br>
Risk: The skill defaults to applying clear documentation fixes unless report-only mode is requested. <br>
Mitigation: Request report-only mode when you want recommendations without edits, and review generated diffs before merging changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-stewardship) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with prompts, checklists, and optional code or documentation change proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect repository documentation and agent-instruction files, and may suggest or apply clear documentation fixes unless report-only mode is requested.] <br>

## Skill Version(s): <br>
1.9.13 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
