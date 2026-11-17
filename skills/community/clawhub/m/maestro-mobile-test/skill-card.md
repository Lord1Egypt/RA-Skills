## Description:

Write and run end-to-end tests for React Native and Expo apps using Maestro CLI on Android emulators or iOS simulators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, run, and troubleshoot Maestro flows for native React Native and Expo application journeys, including emulator setup, adb reverse networking, headed authoring, and CI-oriented runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified internet-downloaded code and privileged installers.

Mitigation: Review setup before running it, install Maestro from a pinned and verified release where possible, run as an unprivileged user, and approve any sudo or package-manager steps deliberately.

Risk: CI examples can introduce supply-chain risk if installers or third-party actions are copied without pinning and verification.

Mitigation: Pin and verify external installers and CI actions before adopting the example workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/maestro-mobile-test)
- [Maestro documentation](https://maestro.mobile.dev)
- [Maestro CLI test suites and reports](https://maestro.mobile.dev/cli/test-suites-and-reports)
- [Maestro flow API reference](https://maestro.mobile.dev/reference/api)
- [Maestro repository](https://github.com/mobile-dev-inc/maestro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, shell command, and CI configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or suggest Maestro flow files and setup/run commands for the user's mobile app environment.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
