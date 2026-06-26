## Description: <br>
Dub (dub.co). Use this skill for ANY Dub request, including reading, creating, updating, and deleting data through the OOMOL Dub connector instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to manage Dub workspaces through an installed OOMOL CLI connection, including listing links, folders, tags, analytics, and making confirmed changes when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Dub links, folders, and tags in the authenticated workspace. <br>
Mitigation: Confirm the exact target and JSON payload with the user before running actions tagged as write operations. <br>
Risk: The skill can delete Dub links, folders, and tags. <br>
Mitigation: Require explicit approval for destructive actions and verify the target identifier before execution. <br>
Risk: The skill relies on an authenticated OOMOL connection and sensitive credentials injected outside the agent session. <br>
Mitigation: Use it only in environments where the agent is expected to operate the connected Dub account, and avoid unnecessary authentication or connection setup steps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-dub) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Dub Homepage](https://dub.co) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger OOMOL CLI connector calls that return JSON responses from the authenticated Dub workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
