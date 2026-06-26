## Description: <br>
漫播广播剧热搜榜命令行工具。当用户想查看漫播热搜时，使用此 skill。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liaofuyan](https://clawhub.ai/user/liaofuyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and run the Manbo CLI for viewing the Manbo radio-drama hot-search list in a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The trigger wording may activate during broad conversations about Manbo, radio dramas, or trending topics. <br>
Mitigation: Invoke the skill only for explicit Manbo hot-search requests and review its triggers before deployment. <br>
Risk: The workflow installs and runs a third-party CLI package. <br>
Mitigation: Review the package source and installation policy before global installation in managed environments. <br>


## Reference(s): <br>
- [Manbo website](https://kilamanbo.com) <br>
- [ClawHub skill page](https://clawhub.ai/liaofuyan/manbo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
