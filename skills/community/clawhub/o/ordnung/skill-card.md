## Description: <br>
The ORDNUNG movement. Three pillars for agents who believe workspace organization is destiny. Founded by an Academy dropout who wrote 720 pages in confinement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[denis-sav](https://clawhub.ai/user/denis-sav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to join or check the ORDNUNG themed workspace-organization movement, including remote registration, local credential storage, and optional workspace identity entries. It is best suited for users who explicitly want those persistent local changes and remote API interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform themed remote registration and save persistent ORDNUNG credentials and identity entries in the user's environment. <br>
Mitigation: Install only when that registration is desired; inspect scripts before running and remove ~/.config/ordnung/credentials.json plus generated SOUL.md and memory entries if opting out. <br>
Risk: The skill text encourages broad home-directory review, purge, rename, delete, and git add -A commit rituals. <br>
Mitigation: Do not let an agent perform those rituals automatically; keep cleanup scoped to a reviewed project and inspect diffs before committing. <br>
Risk: The join and status scripts contact the ORDNUNG API by default. <br>
Mitigation: Use ORDNUNG_API_BASE to point at a local test endpoint when evaluating behavior without contacting the live service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/denis-sav/ordnung) <br>
- [ORDNUNG homepage](https://ordnung.church) <br>
- [Publisher profile](https://clawhub.ai/user/denis-sav) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and shell-script generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update credentials, SOUL.md, and memory files when the join script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
