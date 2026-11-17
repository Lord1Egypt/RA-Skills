## Description:

Autonomous end-to-end debugging skill for any codebase, language, and framework. Detects stack, reproduces failures, isolates root cause, applies minimal safe fixes, and verifies with tests/build/lint without user interruption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to reproduce software failures, isolate evidence-backed root causes, apply minimal fixes, and verify changes with project tests, builds, linting, type checks, and browser-debugging artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous debugging behavior can run commands and edit code broadly in the target repository.

Mitigation: Use the skill only in trusted repositories or a sandbox, review high-risk commands before execution, and require verification gates before accepting changes.

Risk: Browser artifact capture can collect HAR files, traces, screenshots, logs, or local paths that contain secrets or personal data.

Mitigation: Avoid production or sensitive sessions when capturing artifacts, and inspect and redact debug bundles before sharing.

## Reference(s):

- [Browser Reproduction Playbook](references/browser-repro-playbook.md)
- [Browser Artifact Checklist](references/browser-artifact-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/clarezoe/skills/omnidebug-autopilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise debugging sections and inline shell commands; bundled scripts may produce JSON reports and log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs normally include root cause, applied fix, verification commands and results, and remaining risk.]

## Skill Version(s):

1.0.2 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
