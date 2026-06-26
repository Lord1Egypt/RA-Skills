## Description: <br>
Guides agents through safe Java feature, refactor, or bugfix changes using minimal diffs, targeted tests, and PR-ready evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanerilyazov](https://clawhub.ai/user/tanerilyazov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when asking an agent to make Java feature, refactor, or bugfix changes that need reviewable implementation steps, test evidence, and PR-ready summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-produced Java changes may be incorrect, incomplete, or broader than the requested acceptance criteria. <br>
Mitigation: Review the diff before committing and keep implementation scoped to the smallest change that satisfies the stated criteria. <br>
Risk: The workflow may run project test commands such as Maven tests in the target repository. <br>
Mitigation: Use the skill only in repositories you trust and record the exact commands and results for reviewer verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanerilyazov/java-change-with-tests) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with implementation plan, changed-file summary, command results, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes exact verification commands and results when tests are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
