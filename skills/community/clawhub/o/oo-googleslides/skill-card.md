## Description: <br>
Google Slides (workspace.google.com). Use this skill for ANY Google Slides request - reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to read, create, copy, update, and inspect Google Slides presentations through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Google Slides through an OOMOL-connected account. <br>
Mitigation: Install and use it only when that account-level access is intended. <br>
Risk: Write actions, especially raw batchUpdate requests, can change presentation content or structure. <br>
Mitigation: Review the exact payload and expected effect with the user before approving write actions. <br>
Risk: The first-time setup path includes a remote CLI installer command. <br>
Mitigation: Verify the OOMOL CLI installer source before running the install command. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-googleslides) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Google Slides](https://workspace.google.com/products/slides/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions return JSON data with execution metadata when run through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
