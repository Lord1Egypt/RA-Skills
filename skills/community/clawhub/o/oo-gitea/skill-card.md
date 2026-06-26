## Description: <br>
This skill lets agents operate Gitea through an OOMOL-connected account for repository discovery, issue workflows, and approved issue or comment creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to inspect Gitea account, repository, issue, and comment data through an OOMOL-connected Gitea account. With explicit confirmation, it can also create issues and issue comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Gitea account and repository information through the connected OOMOL account. <br>
Mitigation: Connect only a Gitea account whose repositories you are comfortable exposing to this connector. <br>
Risk: The skill can create Gitea issues and issue comments when write actions are approved. <br>
Mitigation: Review the exact payload and expected effect before allowing any write action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-gitea) <br>
- [Gitea product page](https://about.gitea.com/products/gitea/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return JSON data from Gitea connector actions when commands are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
