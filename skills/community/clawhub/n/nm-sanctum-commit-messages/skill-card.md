## Description: <br>
Generates conventional commit messages from staged changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect staged Git changes and draft a conventional commit message with a concise subject, body, and optional footer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect staged diffs on broad Git-related requests. <br>
Mitigation: Confirm that commit-message drafting is intended before allowing the agent to read staged changes. <br>
Risk: The skill writes a local commit_msg.txt draft that may not match the user's intent. <br>
Mitigation: Review the generated subject, body, and footer before using the message in a commit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-sanctum-commit-messages) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown text with a local commit_msg.txt file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts conventional commit subject, body, and footer; previews the result for review.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
