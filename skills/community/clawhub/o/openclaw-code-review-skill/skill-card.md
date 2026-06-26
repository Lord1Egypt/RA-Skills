## Description: <br>
Reviews Pull Requests or code diffs with parallel agent checks and confidence scoring to filter likely false positives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdapic](https://clawhub.ai/user/cdapic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review GitHub pull requests or pasted diffs before merge, focusing on guideline compliance, obvious bugs, security-sensitive changes, and useful git history context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional PR comment workflow can publish generated review text to a GitHub repository. <br>
Mitigation: Review the generated text for secrets, internal details, and accuracy before asking the agent to post it. <br>
Risk: The skill relies on GitHub CLI access to read PR data and, when requested, post comments. <br>
Mitigation: Use an authenticated GitHub CLI account with repository permissions appropriate for the review task. <br>
Risk: Automated review findings may be incomplete or incorrect even with confidence filtering. <br>
Mitigation: Treat findings as a starting point for human code review, especially for security-sensitive or high-impact changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cdapic/openclaw-code-review-skill) <br>
- [Publisher profile](https://clawhub.ai/user/cdapic) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [GitHub CLI](https://cli.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with optional GitHub PR comment body and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters reported findings by confidence threshold and can produce public PR comments when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
