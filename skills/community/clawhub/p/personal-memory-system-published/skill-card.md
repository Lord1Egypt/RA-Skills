## Description: <br>
Personal Memory System syncs a local MEMORY.md file into a SQLite memory.db so an agent can search and summarize long-term personal notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awublack](https://clawhub.ai/user/awublack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to persist personal decisions, insights, and notes in a local Markdown file while making those memories queryable through SQLite-backed retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync script uses hard-coded /home/awu workspace paths. <br>
Mitigation: Change the MEMORY.md and memory.db paths to the target workspace before enabling the skill. <br>
Risk: The sync script deletes and rebuilds the memories table when MEMORY.md is newer than memory.db. <br>
Mitigation: Back up any existing memory.db and only enable heartbeat syncing after confirming this rebuild behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/awublack/personal-memory-system-published) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and SQLite workflow details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and usage guidance; the bundled script updates a local SQLite database from MEMORY.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
