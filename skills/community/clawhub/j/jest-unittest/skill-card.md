## Description: <br>
jest-unittest routes Jest component testing requests to sub-skills that check coverage, complete tests toward 100% coverage, and diagnose or repair failing unit tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vuact](https://clawhub.ai/user/vuact) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers working on Jest-based front-end projects use this skill to configure test analysis, identify components below full coverage, generate or update tests, and diagnose failing tests or console warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unvalidated component names can influence shell commands and cleanup paths when running Jest helper scripts. <br>
Mitigation: Install only in trusted Jest projects, avoid untrusted component names or generated configuration, and review all proposed test edits before committing. <br>
Risk: Shell-string execution increases impact if configuration or component names are malicious. <br>
Mitigation: Validate component names, constrain cleanup paths to the intended coverage directory, and replace shell-string execution with argument-array execution before treating the release as low risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vuact/jest-unittest) <br>
- [Publisher profile](https://clawhub.ai/user/vuact) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON script output summaries, and possible Jest test file edits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Jest test files and project-scoped .temp configuration and coverage files; helper scripts emit JSON for coverage and test diagnostics.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
