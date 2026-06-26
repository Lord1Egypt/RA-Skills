## Description: <br>
Guides agents in using Apple's first-party testing tools for iOS and macOS projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soponcd](https://clawhub.ai/user/soponcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to plan, write, and run Apple platform unit, UI, snapshot, performance, and accessibility tests with XCTest, XCUITest, Instruments, and a project-local test wrapper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to use a repository-local test wrapper, which may behave differently in unfamiliar projects. <br>
Mitigation: Review ./tools/run_native_tests.sh before running it and limit execution to trusted Apple development repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soponcd/native-automation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and XCTest/XCUITest code patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Relies on the target repository's ./tools/run_native_tests.sh modes when executing tests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
