## Description: <br>
Stop before you break: four mandatory checks before every operation, covering search, rollback, testing, and scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p9sgr2rnrj-ux](https://clawhub.ai/user/p9sgr2rnrj-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent users, and teams use this skill to pause before commands, deployments, configuration changes, or unfamiliar operations and confirm search, rollback, validation, and impact scope before proceeding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package can make persistent shell startup changes through install.sh. <br>
Mitigation: Review install.sh before running it, especially PATH edits, or install manually into an explicit directory. <br>
Risk: publish.sh can use a logged-in ClawHub session to publish this package. <br>
Mitigation: Do not run publish.sh unless publication is intentional and the active ClawHub account is correct. <br>
Risk: The workflow could trigger when the user did not intend to start a preflight gate. <br>
Mitigation: Use an explicit command-style trigger for agent workflows before applying the checklist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/p9sgr2rnrj-ux/preflight-workflow) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional interactive shell prompts and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive checklist flow; the CLI script exits non-zero when any required preflight check fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
