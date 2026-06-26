## Description: <br>
CloudConvert helps agents operate CloudConvert through an OOMOL-connected account by inspecting live connector schemas and running CloudConvert actions with the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage CloudConvert jobs, tasks, conversion types, and account information from an agent workflow. It supports read actions, state-changing actions, and destructive delete actions with confirmation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evidence security verdict is suspicious and notes powerful maintainer or moderation workflows. <br>
Mitigation: Install only when the intended workflow matches the release purpose, review the skill before use, and run production-affecting commands only with the correct account and confirmed target. <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected CloudConvert account. <br>
Mitigation: Use server-side credential injection, avoid handling raw tokens directly, and confirm write or destructive CloudConvert actions before execution. <br>


## Reference(s): <br>
- [CloudConvert homepage](https://cloudconvert.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-cloudconvert) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute CloudConvert connector actions through the oo CLI when the user has configured the required account connection.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
