## Description: <br>
Use this Ninox skill for reading, creating, updating, and deleting Ninox data through an OOMOL-connected oo CLI workflow instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Ninox workspaces, databases, tables, and records through an OOMOL-connected oo CLI workflow. It supports read actions, record creation or updates, and explicitly approved destructive record deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks this release as suspicious and reports a helper that can run nested Codex review with approval and sandbox bypass enabled. <br>
Mitigation: Install only in trusted ClawHub maintainer workflows; when using autoreview, run it with --no-yolo or AUTOREVIEW_YOLO=0 unless unrestricted nested Codex access is acceptable. <br>
Risk: The skill can create, update, or delete Ninox records when write or destructive actions are invoked. <br>
Mitigation: Confirm exact payloads and targets before write actions, and require explicit approval before destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-ninox) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Ninox homepage](https://ninox.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, an authenticated OOMOL account, and a connected Ninox credential.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
