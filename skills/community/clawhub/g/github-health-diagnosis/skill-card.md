## Description: <br>
Analyzes a GitHub repository's issues, code quality, CI status, community activity, and security posture, then generates a health report and publishes it to Feishu Wiki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical leads, maintainers, and evaluators use this skill to assess repository health across code quality, issue activity, CI/CD status, community activity, and security. It produces shareable report artifacts and a Feishu Wiki page for team review and documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository health reports may include sensitive issue, code quality, CI/CD, or security findings and are automatically published to Feishu Wiki. <br>
Mitigation: Use the skill first on public or low-sensitivity repositories, provide an explicit Wiki space and parent node, and confirm the intended destination before publishing. <br>
Risk: GitHub and Feishu credentials can expose more repositories or Wiki spaces than intended if broadly scoped. <br>
Mitigation: Restrict credentials to the exact repositories and Feishu spaces required for the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/github-health-diagnosis) <br>
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen) <br>
- [Skill README](artifact/README.md) <br>
- [Workflow definition](artifact/workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, API Calls] <br>
**Output Format:** [Feishu Wiki page, diagnostic card images, structured scores, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes repository findings to Feishu Wiki and can return cover and detail diagnostic cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
