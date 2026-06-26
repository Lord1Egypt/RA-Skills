## Description: <br>
Provides SmugMug search and read access through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search and browse SmugMug users, folders, albums, nodes, images, image sizes, and metadata through an OOMOL-connected SmugMug account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OOMOL as an intermediary for SmugMug access and server-side credential handling. <br>
Mitigation: Install and connect the skill only after confirming that OOMOL is an acceptable intermediary for the SmugMug account. <br>
Risk: First-time setup may require installing the oo CLI from an external OOMOL installer URL. <br>
Mitigation: Run the one-time installer only from the documented source and only when the CLI is actually missing. <br>
Risk: Connector commands can access data from the connected SmugMug account. <br>
Mitigation: Inspect each action schema before building payloads and use the documented read-only actions unless the user explicitly approves a future write or destructive action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-smugmug) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [SmugMug homepage](https://www.smugmug.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON connector payloads or responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-oriented connector actions return JSON data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
