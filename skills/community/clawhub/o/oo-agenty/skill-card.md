## Description: <br>
Agenty lets an agent operate Agenty through an OOMOL-connected account for reading, creating, updating, and deleting Agenty data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Agenty agents, jobs, lists, and web utility actions through the OOMOL oo CLI after connecting their Agenty account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform meaningful account-level actions in Agenty, including write and destructive operations. <br>
Mitigation: Review the exact payload and effect before approving write actions, and require explicit approval before destructive actions such as clearing lists, deleting rows, or deleting agents. <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected Agenty account. <br>
Mitigation: Install only when the user intends to let Codex operate that Agenty account through OOMOL, and avoid exposing raw tokens in prompts or files. <br>


## Reference(s): <br>
- [Agenty homepage](https://agenty.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-agenty) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; command responses may include Agenty data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
