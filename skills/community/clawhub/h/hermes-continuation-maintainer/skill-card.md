## Description:

Diagnose and repair Hermes Agent runs that silently stop and require manual "continue" messages even though no user input is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis9087](https://clawhub.ai/user/hollis9087)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose Hermes continuation stalls, classify recent text-stop behavior, and apply focused runtime fixes only when scanner evidence supports the change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads Hermes logs and the Hermes state database, which may include private conversation content.

Mitigation: Run the scanner only in a private terminal and avoid sharing full JSON or text output in tickets, chat, or CI logs.

Risk: Continuation-loop patches can change when Hermes decides to keep acting without user input.

Mitigation: Apply patches only after scanner evidence identifies continuation candidates, review proposed runtime edits, and run the focused regression checks before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hollis9087/skills/hermes-continuation-maintainer)
- [Publisher profile](https://clawhub.ai/user/hollis9087)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Concise Markdown report with scanner counts, file changes, test commands, and restart guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deterministic scanner classifications and proposed patches for Hermes runtime files.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
