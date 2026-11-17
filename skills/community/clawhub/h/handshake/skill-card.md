## Description:

Open or close a branch-scoped project handshake that preserves compact context, relevant skills, unresolved work, and ordered next actions. Use when starting or ending a Claude Code work session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[housealone](https://clawhub.ai/user/housealone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Handshake to preserve concise, branch-scoped session context between Claude Code or Codex work sessions, including unresolved work, relevant skills, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handshake files may capture sensitive project context in local session notes.

Mitigation: Review saved handshakes when working on sensitive repositories and avoid recording secrets or private credentials.

Risk: A stale or edited handshake could mislead the next work session.

Mitigation: Treat handshake content as editable notes and verify file anchors and repository state before acting on it.

Risk: Closing a session replaces the previous handoff file for the same project and branch.

Mitigation: Confirm the current project and branch before closing a session, and preserve important prior handoffs separately when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/housealone/skills/handshake)
- [Server-resolved GitHub source](https://github.com/HouseAlone/handshake-skill/tree/main/skills/handshake)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or reads one local branch-scoped handshake file per project.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
