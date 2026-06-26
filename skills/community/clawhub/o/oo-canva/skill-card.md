## Description: <br>
Canva (canva.com). Use this skill for any Canva request: reading, creating, and updating data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent read and manage Canva resources through an OOMOL-connected Canva account, including design creation, export jobs, asset uploads, folder operations, and metadata lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform Canva write operations such as creating designs, starting exports, uploading URL assets, creating folders, and moving folder items. <br>
Mitigation: Review the exact action payload and expected Canva effect with the user before approving write operations. <br>
Risk: The skill requires a connected Canva account through OOMOL and may rely on sensitive OAuth-backed credentials. <br>
Mitigation: Install and use it only when OOMOL access is intended, and run login or connection setup only after an authentication or connection failure. <br>


## Reference(s): <br>
- [Canva homepage](https://www.canva.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-canva) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may produce Canva connector responses, job identifiers, status results, and setup guidance through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
