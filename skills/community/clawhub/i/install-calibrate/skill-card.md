## Description:

Install, configure, verify, or troubleshoot the Calibrate browser SDK and standalone sidecar in JavaScript or TypeScript applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ojusave](https://clawhub.ai/user/ojusave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to add Calibrate to supported JavaScript or TypeScript browser applications, map onboarding routes, configure collector access, and verify integration evidence. It is intended for guided project changes that require review before applying generated files or running commands with credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly invokes an unpinned npm CLI that can edit project files.

Mitigation: Review the CLI source or use a pinned, lockfile-controlled `usecalibrate` version before installation; preview plans and file diffs before approving writes.

Risk: Collector verification can involve Calibrate write keys or other scoped credentials.

Mitigation: Use disposable scoped keys, pass secrets through environment variables rather than command arguments, and avoid production secrets unless the CLI version and source are trusted.

Risk: Unsupported, ambiguous, or custom integrations may lead to incorrect changes or incomplete verification claims.

Mitigation: Require explicit user approval for route decisions and generated changes, preserve partial failures, and report only the verification level supported by completed checks.

## Reference(s):

- [Calibrate Installer CLI](references/cli.md)
- [Server-resolved source repository](https://github.com/ojusave/usecalibrate/tree/main/packages/kit/skills/install-calibrate)
- [ClawHub skill page](https://clawhub.ai/ojusave/skills/install-calibrate)
- [Publisher profile](https://clawhub.ai/user/ojusave)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown guidance with inline shell commands, file diffs, configuration instructions, and verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a Calibrate plan file, generated integration files, dependency commands, environment-variable guidance, and one declared verification level.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
