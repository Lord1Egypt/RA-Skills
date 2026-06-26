## Description: <br>
Defines the contract for deferred-item capture across plugins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to build or validate deferred-capture wrappers, source labels, and issue templates for plugin workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Issue bodies or artifact paths produced by wrappers based on this contract may contain private paths or sensitive context. <br>
Mitigation: Review issue content before filing and use dry-run mode when testing wrappers. <br>
Risk: Wrappers that implement the contract can target the wrong repository or create duplicate deferred issues. <br>
Mitigation: Confirm the target repository and duplicate-detection behavior before using an implementation outside dry-run mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-deferred-capture) <br>
- [Leyline plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline command examples and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no bundled executable behavior.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
