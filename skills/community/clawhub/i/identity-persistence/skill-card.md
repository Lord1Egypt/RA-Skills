## Description:

Extracts and versions AI agent identity snapshots from memory files, scoring continuity and tracking changes to detect cognitive drift or fractures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quriustus](https://clawhub.ai/user/quriustus)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create versioned identity snapshots from agent memory files, compare continuity over time, and prepare pre-upgrade identity freezes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads identity, memory, user, tool, and heartbeat files that may contain sensitive agent or user information.

Mitigation: Run only in workspaces where that content is intended to be processed; review and redact source files before execution.

Risk: The skill sends raw workspace content to Google's Gemini API.

Mitigation: Use an approved API account and data-handling policy; avoid running it on confidential material unless external processing is permitted.

Risk: The skill stores derived identity snapshots and diffs locally.

Mitigation: Protect or delete generated snapshot and diff files according to the workspace's retention requirements.

Risk: The script reads a local Google token from a fixed OpenClaw auth profile.

Mitigation: Check credential scope and prefer a version that lets the operator supply and rotate the API key explicitly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quriustus/skills/identity-persistence)

## Skill Output:

**Output Type(s):** [text, JSON files, shell commands, guidance]

**Output Format:** [Markdown guidance with bash examples; runtime output includes terminal text and JSON identity snapshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes current identity, versioned snapshots, and diffs under the configured workspace identity directory.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
