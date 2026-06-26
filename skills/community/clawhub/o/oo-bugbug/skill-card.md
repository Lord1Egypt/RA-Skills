## Description: <br>
BugBug helps agents inspect BugBug connector schemas, read workspace data, and run BugBug tests through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and support agents use this skill to inspect BugBug action schemas, read suites, tests, profiles, and test-run data, and launch BugBug test runs through a connected workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute BugBug tests even though its short description emphasizes searching and reading data. <br>
Mitigation: Use it only where launching BugBug test runs is acceptable, and require explicit user confirmation before invoking run_test. <br>
Risk: The skill depends on the oo CLI, OOMOL sign-in, and a connected BugBug account. <br>
Mitigation: Do not initiate installation, sign-in, or connection setup proactively; perform those steps only after a matching failure and explicit user confirmation. <br>


## Reference(s): <br>
- [BugBug homepage](https://bugbug.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub BugBug skill page](https://clawhub.ai/oomol/oo-bugbug) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an OOMOL sign-in, and a connected BugBug workspace; some actions can launch BugBug test runs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
