## Description: <br>
Npc Distill Main helps an agent build local, anonymized persona memory files from a specific person's communications so users can rehearse reports, pressure-test plans, draft materials, and anticipate likely decision concerns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bangbangmao666666](https://clawhub.ai/user/bangbangmao666666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agent users use this skill to turn meeting notes, messages, emails, or web content into local persona evidence, then rehearse conversations, pressure-test plans, and draft materials aligned to the modeled person's preferences. The skill is intended for private preparation and review, not for impersonating the person or claiming to predict their actual decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates durable local profiles and rehearsal notes from potentially sensitive workplace communications. <br>
Mitigation: Use it only with authorized data, keep memory files out of shared folders and public repositories, and consider device or disk encryption for the storage location. <br>
Risk: Persona evidence is stored in plaintext Markdown files and may persist in backups or archives. <br>
Mitigation: Delete the active memory file, backups, and archived files when the profile is no longer needed. <br>
Risk: Drafts and rehearsals may be mistaken for the real person's views or decisions. <br>
Mitigation: Treat outputs as preparation aids, preserve disclaimers that simulations do not represent the person's actual opinion, and review every diff before writing memory updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bangbangmao666666/npc-distill-main) <br>
- [Publisher profile](https://clawhub.ai/user/bangbangmao666666) <br>
- [Project homepage from metadata](https://github.com/clawhub/npc-distill) <br>
- [Agent skills compatibility reference](references/agentskills-compat.md) <br>
- [Memory format reference](references/memory-format.md) <br>
- [agentskills.io compatibility standard](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, local Markdown memory files, diffs, JSON extraction outputs, and shell commands for helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores persona evidence and rehearsal notes in local plaintext Markdown files using anonymized IDs such as L001 and L002.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version is 0.2.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
