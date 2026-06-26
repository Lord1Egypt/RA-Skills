## Description: <br>
Outline helps agents search and read Outline workspace content through an OOMOL-connected account instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to retrieve, list, and search Outline collections and documents available through their OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected account with access to Outline content. <br>
Mitigation: Install only when the agent should search and read Outline content available through that connected account. <br>
Risk: First-time setup may require installing the oo CLI. <br>
Mitigation: Review the oo CLI installer before setup and only run setup steps after an authentication, connection, or missing-command error. <br>
Risk: Future connector actions tagged write or destructive could alter Outline data. <br>
Mitigation: Require explicit user approval for the exact payload and effect before allowing any write or delete action. <br>


## Reference(s): <br>
- [Outline homepage](https://www.getoutline.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to return Outline connector responses as JSON when actions are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
