## Description: <br>
Loci provides a structured local memory system for AI agents using domains, decay, links, recall, maintenance, pruning, and export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bayhax](https://clawhub.ai/user/bayhax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Loci to store durable context, recall prior decisions or preferences, maintain memory health with heartbeat walks, and migrate away from flat memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-lived local memories on disk, which may retain secrets, credentials, regulated data, or sensitive personal details if users choose to store them. <br>
Mitigation: Avoid storing sensitive data unless retention is intentional, and periodically review, export, prune, or delete the palace file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bayhax/loci) <br>
- [loci GitHub repository](https://github.com/bayhax/loci) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown export, and JSON memory data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and updates a local palace JSON file by default at ~/.openclaw/workspace/loci_palace.json; supports an alternate path with --palace.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
