## Description: <br>
Operates Databar.ai through the OOMOL oo CLI for reading tables, creating tables, inserting rows, and running enrichment or waterfall tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Databar.ai tables and submit enrichment or waterfall jobs from an agent through their connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create tables and insert rows in Databar.ai, so mistaken payloads can change workspace data. <br>
Mitigation: Confirm the exact payload and expected effect with the user before write actions, and inspect the live action schema before running commands. <br>
Risk: Broad activation wording may cause an agent to use Databar.ai for loosely related requests. <br>
Mitigation: Be explicit when requesting Databar.ai work and review proposed connector actions before approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-databar-ai) <br>
- [Databar.ai Homepage](https://databar.ai/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI connector schemas before execution; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
