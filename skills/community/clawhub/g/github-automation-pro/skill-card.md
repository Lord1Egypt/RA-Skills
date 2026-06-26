## Description: <br>
Automates GitHub issue management, pull request analysis, release creation, and repository analytics for agents using a configured GitHub token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy825lay-tech](https://clawhub.ai/user/andy825lay-tech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and repository maintainers use this skill to automate routine GitHub workflows such as creating and updating issues, analyzing pull requests, publishing releases, and checking repository health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a GitHub token while shipping obfuscated JavaScript. <br>
Mitigation: Use a fine-grained token scoped only to the target repository and required permissions, and revoke it after use. <br>
Risk: Configured actions can create or update GitHub issues and releases. <br>
Mitigation: Verify the owner, repository, action, and parameters before allowing write operations. <br>
Risk: The artifact includes off-platform crypto payment and license-key claims. <br>
Mitigation: Do not rely on those claims unless the publisher and payment path are independently verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy825lay-tech/github-automation-pro) <br>
- [Publisher profile](https://clawhub.ai/user/andy825lay-tech) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON-style result objects with Markdown guidance, code examples, and shell commands where applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitHub token and repository owner/repo configuration; some actions can create or modify GitHub issues and releases.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
