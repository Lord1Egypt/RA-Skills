## Description: <br>
Autonomous end-to-end debugging skill for any codebase, language, and framework. Detects stack, reproduces failures, isolates root cause, applies minimal safe fixes, and verifies with tests/build/lint without user interruption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent reproduce software failures, collect debugging evidence, identify root cause, apply a minimal fix, and verify the result with project-appropriate quality gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to run project commands and modify files autonomously during debugging. <br>
Mitigation: Use it in a sandbox or disposable workspace for untrusted code and review commands or diffs before accepting changes when possible. <br>
Risk: Browser debugging flows can collect screenshots, traces, HAR files, logs, and other local artifacts that may contain sensitive data. <br>
Mitigation: Inspect and redact .debug outputs before sharing them outside the workspace. <br>
Risk: Autonomous root-cause fixes may affect project behavior if the reproduction or verification gate is incomplete. <br>
Mitigation: Require deterministic reproduction, targeted regression coverage, and applicable test, lint, typecheck, build, or smoke verification before treating the fix as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clarezoe/omnidebug-autopilot) <br>
- [Browser Reproduction Playbook](references/browser-repro-playbook.md) <br>
- [Browser Artifact Checklist](references/browser-artifact-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with root cause, applied fix, verification commands, and remaining risk; may include code diffs and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local project files and local debug artifacts such as logs, screenshots, traces, HAR files, and verification reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
