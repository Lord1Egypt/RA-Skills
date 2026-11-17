## Description:

Conversational interface for semantic book search as a companion skill for the Librarian project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nonlinear](https://clawhub.ai/user/nonlinear)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to ask natural-language questions against a local Librarian book library, infer a topic or book scope, and receive cited search results or clear hard-stop messages when the search cannot run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad conversational triggers plus local shell execution may cause the skill to search local Librarian indexes when a user did not intend it.

Mitigation: Prefer narrowing activation to explicit librarian commands and review trigger behavior before installation.

Risk: The security summary flags an unsafe temporary file pattern in librarian.sh.

Mitigation: Update librarian.sh to use mktemp and direct array execution before using the skill with private libraries.

Risk: The skill searches local book indexes that may contain private library content.

Mitigation: Install only when local index access is acceptable and limit use to trusted workspaces.

## Reference(s):

- [Librarian project](https://github.com/nonlinear/librarian)
- [ClawHub skill page](https://clawhub.ai/nonlinear/skills/librarian)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown responses with citations, hard-stop messages, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Librarian metadata and search indexes; successful searches include cited excerpts and source information.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json and SKILL.md report 0.15.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
