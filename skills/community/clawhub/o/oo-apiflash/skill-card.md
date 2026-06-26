## Description: <br>
ApiFlash helps agents operate ApiFlash through an OOMOL-connected account to capture website screenshots, check quota information, and retrieve screenshot metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run ApiFlash screenshot and quota actions through the oo CLI after connecting an OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require installing or using the oo CLI before actions can run. <br>
Mitigation: Install the CLI only from trusted OOMOL documentation, inspect remote installer scripts before execution, or use a pinned package when available. <br>
Risk: The skill operates through connected ApiFlash credentials. <br>
Mitigation: Use it only when the user intends to access ApiFlash through an OOMOL-connected account and follow the skill's auth recovery steps only after a command fails. <br>


## Reference(s): <br>
- [ApiFlash ClawHub page](https://clawhub.ai/oomol/oo-apiflash) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ApiFlash homepage](https://apiflash.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return ApiFlash screenshot URLs, quota details, screenshot metadata, and oo CLI recovery guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
