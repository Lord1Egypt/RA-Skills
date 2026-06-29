## Description: <br>
Generates conventional commit messages from staged changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to inspect staged Git changes, classify the change type, and draft a human-readable conventional commit message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read staged diffs that include private code or sensitive changes. <br>
Mitigation: Run it only in repositories where the agent is allowed to inspect staged changes, and review the generated message before use. <br>
Risk: The workflow may create or overwrite ./commit_msg.txt. <br>
Mitigation: Check the file after generation and use a more specific invocation if the agent environment supports constraining file writes. <br>


## Reference(s): <br>
- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands and a conventional commit message draft.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write the drafted message to ./commit_msg.txt for review.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
