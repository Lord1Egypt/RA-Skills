## Description: <br>
Deprecated compatibility alias for the canonical `opencli` skill, intended only for older notes, memory, or prompts that still refer to `opencli-exec`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this compatibility alias when legacy workspace material still invokes `opencli-exec`, then route current work through the canonical `opencli` skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The alias forwards all arguments to a separately installed local Opencli script, so an unexpected or missing canonical path could run the wrong target or fail. <br>
Mitigation: Install only when the legacy alias is needed, verify the disclosed canonical Opencli path exists, and confirm it points to the expected installation before use. <br>


## Reference(s): <br>
- [Deprecated alias command reference](references/commands.md) <br>
- [ClawHub skill page](https://clawhub.ai/chaoyang78/opencli-exec) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forwards command arguments to a separately installed canonical Opencli script.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
