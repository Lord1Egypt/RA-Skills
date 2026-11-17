## Description:

KaiwuDB database source build and test skill for configuring, compiling, installing, and running C++ or Go unit tests with CMake.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdb](https://clawhub.ai/user/kwdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers working in a trusted KaiwuDB checkout use this skill to choose supported build options, run CMake builds, and execute C++ or Go unit tests after confirming paths and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup steps can delete unintended local files if the source directory or GOPATH is wrong.

Mitigation: Use the skill only in a trusted KaiwuDB checkout, require validated absolute paths, and show the fully resolved deletion targets before cleanup runs.

Risk: Test scripts can execute unintended local files when path resolution or discovered test files are not controlled.

Mitigation: Confirm the exact source directory before execution, quote and validate script inputs, and review discovered test targets before running them.

Risk: The release evidence security verdict is suspicious because the workflow depends on broad cleanup and local script execution.

Mitigation: Review the skill before installing and harden scripts to fail on directory-change errors, quote variables, and avoid broad rm -rf globs.

## Reference(s):

- [KWDB Build ClawHub listing](https://clawhub.ai/kwdb/skills/kwdb-build)
- [Build Questions](references/build-questions.md)
- [CMake Options](references/cmake-options.md)
- [C++ Unit Test](references/cpp-unittest.md)
- [Go Unit Test](references/golang-unittest.md)
- [Dependencies](references/dependencies.md)
- [Project Structure](references/project-structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before build or test actions and reports build or test failures without applying automatic fixes.]

## Skill Version(s):

1.2.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
