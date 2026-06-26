## Description: <br>
Leiga (leiga.com). Use this skill for ANY Leiga request -- searching and reading data. Whenever a task involves Leiga, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search and read Leiga projects and issues through an OOMOL-connected account. It supports schema-first Leiga connector calls for listing projects, fetching project details, listing issues, and fetching issues by issue number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OOMOL as an intermediary for Leiga account access. <br>
Mitigation: Install and use it only when OOMOL-mediated Leiga access is acceptable for the deployment. <br>
Risk: First-time setup may involve running installer commands from the shell. <br>
Mitigation: Prefer the official OOMOL install guide, or inspect and verify the installer before running curl-to-bash or PowerShell install commands. <br>


## Reference(s): <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Leiga homepage](https://www.leiga.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector commands can return JSON data from Leiga through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
