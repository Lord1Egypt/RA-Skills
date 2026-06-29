## Description: <br>
Implements hub-and-spoke lazy loading to minimize token usage in large skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to design modular agent skills that load relevant guidance based on user intent, artifacts, platform, language, and token budget. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may cause automatic activation in environments with many skills installed. <br>
Mitigation: Review trigger wording before relying on automatic activation. <br>
Risk: Legacy Python snippets may be unsuitable if copied directly into Python 3.8-3.10 projects. <br>
Mitigation: Review and correct legacy Python examples for the target Python version before reuse. <br>
Risk: Documentation examples include code and shell-command patterns that may not fit a specific repository or workflow. <br>
Mitigation: Review examples as guidance before applying them to project files or running related commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-progressive-loading) <br>
- [Clawdis homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code and shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Modules are intended to be loaded on demand to conserve context.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
