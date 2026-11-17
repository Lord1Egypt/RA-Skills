## Description:

loci provides a structured local memory system with domains, decay, links, recall, and maintenance commands for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bayhax](https://clawhub.ai/user/bayhax)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to store durable context, decisions, preferences, lessons learned, and environment details in a structured local memory palace that can later be recalled, walked, pruned, linked, inspected, or exported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved memories are stored as plaintext local files and may expose secrets or sensitive personal or business data if the palace file or parent directory is not private.

Mitigation: Do not store API keys, passwords, tokens, or highly sensitive data unless the palace file and parent directory permissions are private to the account.

Risk: Long-term memory can retain stale or no-longer-appropriate context after tasks change.

Mitigation: Use walk, inspect, prune, and export reviews periodically, and store only context that is likely to remain useful beyond transient task work.

Risk: Reinitializing with force can erase existing local memories.

Mitigation: Confirm the palace path and preserve any needed export or backup before using forced initialization.

## Reference(s):

- [loci ClawHub skill page](https://clawhub.ai/bayhax/skills/loci)
- [loci GitHub repository](https://github.com/bayhax/loci)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Plain text CLI output, JSON palace data, and optional Markdown or JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores memories as plaintext in a local JSON palace file and requires Node.js with no external package dependencies.]

## Skill Version(s):

1.1.1 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
