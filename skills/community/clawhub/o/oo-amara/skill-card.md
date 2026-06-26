## Description: <br>
Operates an OOMOL-connected Amara account for reading, creating, updating, and deleting Amara data through the oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect Amara schemas and run Amara read, write, and subtitle workflow actions through a connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete Amara data when write or destructive actions are used. <br>
Mitigation: Require explicit user intent and confirm the exact payload, target, and expected effect before running write or destructive actions. <br>
Risk: The skill operates through a connected Amara account and requires sensitive account credentials. <br>
Mitigation: Install it only for intended Amara account operation, rely on the connected credential flow, and avoid exposing raw tokens in prompts, logs, or files. <br>
Risk: Running setup or connection commands unnecessarily can alter authentication or connection state. <br>
Mitigation: Use first-time setup steps only after an oo CLI, authentication, connection, scope, or billing error requires them. <br>


## Reference(s): <br>
- [ClawHub Amara Skill](https://clawhub.ai/oomol/oo-amara) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Amara](https://amara.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should inspect the live connector schema before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
