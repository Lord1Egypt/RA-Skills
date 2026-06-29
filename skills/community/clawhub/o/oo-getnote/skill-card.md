## Description: <br>
Get 笔记 helps an agent operate a user's Get 笔记 account through OOMOL for reading, searching, creating, updating, sharing, tagging, and trashing notes and knowledge-base items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they want an agent to manage Get 笔记 notes and knowledge bases through their connected OOMOL account. It supports read workflows, semantic search, note creation and updates, sharing, tag management, and knowledge-base changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Get 笔记 account state, including creating or updating notes, sharing notes, changing tags, and modifying knowledge-base contents. <br>
Mitigation: Review and approve exact payloads before any write or sharing action, including the intended target and user-visible effect. <br>
Risk: Destructive actions can trash notes or remove tags and knowledge-base associations. <br>
Mitigation: Require explicit user approval for the exact note, tag, or knowledge-base item before destructive actions. <br>
Risk: First-time CLI installation, sign-in, or account connection steps grant tooling access to operate the user's Get 笔记 account. <br>
Mitigation: Run setup or authentication steps only when needed for a failed command and only if the user trusts the OOMOL tooling. <br>


## Reference(s): <br>
- [Get 笔记 Skill Page](https://clawhub.ai/oomol/skills/oo-getnote) <br>
- [Get 笔记 Homepage](https://www.biji.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects that include data and an execution id.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
