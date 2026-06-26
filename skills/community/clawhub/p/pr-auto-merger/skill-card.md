## Description: <br>
Autonomous PR merge agent that scans repositories for approved, CI-passing, mergeable pull requests and can merge them automatically with dry-run, squash, and merge options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanxevo3](https://clawhub.ai/user/lanxevo3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect GitHub repositories for pull requests that appear ready to merge, preview actions in dry-run mode, and optionally automate PR merges in scheduled or agent-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the documented minimum approval safeguard is not actually enforced, which can make live or scheduled merges riskier than expected. <br>
Mitigation: Use dry-run mode unless approval thresholds are fixed or independently enforced, and rely on branch protection for required reviews and status checks. <br>
Risk: Unattended live cron or agent runs can merge repository changes automatically. <br>
Mitigation: Avoid unattended live merges until safeguards are validated, and use a dedicated least-privilege GitHub token limited to the intended repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanxevo3/pr-auto-merger) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output with Markdown command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode is the default; live merges require --no-dry-run, GitHub CLI authentication, and repository merge permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
