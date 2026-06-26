## Description: <br>
Loops is a connector skill for reading, creating, updating, and deleting Loops data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Loops connector schemas and run Loops contact, mailing-list, and event actions through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: State-changing Loops actions can create or update contacts, create custom contact properties, or send events that trigger workflows. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged [write]. <br>
Risk: The delete_contact action can remove Loops contacts. <br>
Mitigation: Require explicit user approval for the target email or userId before running actions tagged [destructive]. <br>
Risk: The skill operates an OOMOL-connected Loops account and requires sensitive account access. <br>
Mitigation: Install and use it only when the user intends the agent to operate that Loops account; review write, delete, and event payloads carefully before approval. <br>
Risk: Connector input and output schemas can change independently of the skill text. <br>
Mitigation: Run oo connector schema for the selected Loops action before building each payload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-loops) <br>
- [Loops homepage](https://loops.so) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, text, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; connector runs return JSON when --json is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
