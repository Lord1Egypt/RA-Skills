## Description:

Reviews GitHub pull requests or pasted diffs with multiple specialized agents, confidence scoring, and optional GitHub PR comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdapic](https://clawhub.ai/user/cdapic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull requests or local diffs before merge, focusing on project guideline compliance, obvious bugs, security issues, and useful git history context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill feeds untrusted PR descriptions, diffs, repository guidance files, and code comments into review agents.

Mitigation: Treat review findings as advisory, inspect them locally, and avoid relying on output from untrusted repositories without human review.

Risk: The skill can use an authenticated GitHub CLI session to read repository metadata, diffs, CLAUDE.md files, and git history.

Mitigation: Run it only where the authenticated account is authorized to access the repository and where sending that context to agents is acceptable.

Risk: The optional comment flow can publish generated review text to a pull request.

Mitigation: Review generated findings before using --comment or otherwise asking the skill to post results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cdapic/skills/openclaw-code-review-skill)
- [claw-code](https://github.com/ultraworkers/claw-code)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown code review report with optional GitHub PR comment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only high-confidence findings and may include file paths, line numbers, confidence scores, and remediation guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
