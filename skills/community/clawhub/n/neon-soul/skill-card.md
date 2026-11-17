## Description:

NEON-SOUL synthesizes an agent identity from memory files by extracting recurring patterns, promoting repeated signals to axioms, and generating SOUL.md with provenance tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:


## Use Case:

External developers and agent operators use NEON-SOUL to synthesize, inspect, audit, and roll back a local SOUL.md identity document from workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible processing of private memory files and OpenClaw main-session conversation logs.

Mitigation: Review local memory and session content before synthesis, remove secrets, keep Ollama local, and use --dry-run before writing outputs.

Risk: The security review notes that a normal synthesis run may create a durable git commit containing SOUL.md.

Mitigation: Run in a test or isolated workspace first, review SOUL.md before accepting changes, and avoid pushing commits until the generated content is approved.

## Reference(s):

- [NEON-SOUL ClawHub listing](https://clawhub.ai/leegitw/skills/neon-soul)
- [Project homepage](https://liveneon.ai)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance, Files]

**Output Format:** [Markdown files, JSON status output, and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes SOUL.md and .neon-soul state/backups in the local workspace; requires Node.js >=22 and local Ollama.]

## Skill Version(s):

0.4.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
