## Description: <br>
Granola (granola.ai). Use this skill for ANY Granola request - searching and reading data. Whenever a task involves Granola, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search and read Granola meeting notes, folders, and optional transcripts through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read meeting notes and optional transcripts from the connected Granola account. <br>
Mitigation: Use it for explicit note, folder, or transcript retrieval requests and review returned meeting content before sharing it further. <br>
Risk: Authentication, connection, or billing setup steps may be needed before the connector can run. <br>
Mitigation: Follow the setup fallback only after a command fails for the matching reason, and review the oo CLI installation and OOMOL connection steps before first use. <br>


## Reference(s): <br>
- [Granola homepage](https://www.granola.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-granola) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only Granola get and list action calls; note retrieval can include transcripts when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
