## Description: <br>
TDD-driven E2E workflow with real Playwright browser screenshots as PR proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newtontech](https://clawhub.ai/user/newtontech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to take one GitHub issue through a test-first E2E workflow, capture before and after Playwright screenshots, and publish visual PR evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can push branches and post PR comments under the user's authenticated GitHub account. <br>
Mitigation: Confirm the repository, branch, PR number, and commits before running git or GitHub CLI commands. <br>
Risk: Before and after screenshots may expose secrets, private data, or internal UI state when published to a branch or PR comment. <br>
Mitigation: Inspect screenshots before publishing and remove or redact sensitive content. <br>


## Reference(s): <br>
- [Testing Patterns](references/testing-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/newtontech/pr-proof-of-work) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow steps, test patterns, screenshot capture code, git and GitHub CLI commands, and PR comment guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
