## Description: <br>
Helps an agent convert a GitHub repository into an OpenClaw skill and publish it to ClawHub, including README analysis, duplicate search, SKILL.md drafting, local file creation, publishing, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to package suitable GitHub projects as OpenClaw skills and publish them to ClawHub with a repeatable review, drafting, and release flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing with a user token can expose credentials or authorize unintended releases. <br>
Mitigation: Use the skill only for explicit target repositories, avoid storing tokens in persistent chats, and require user confirmation before any publish command runs. <br>
Risk: The skill describes patching installed ClawHub CLI files to work around publish errors. <br>
Mitigation: Do not allow automatic CLI patching; review any proposed file modification and prefer updating the CLI or using a supported publish flow. <br>
Risk: Generated SKILL.md content may inaccurately represent a source repository or its license. <br>
Mitigation: Review the draft skill, source README, duplicate-search results, and license evidence before writing files or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antonia-sz/github-to-clawhub) <br>
- [Publisher profile](https://clawhub.ai/user/antonia-sz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated SKILL.md content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local skill files and propose ClawHub publish commands when explicitly authorized.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
