## Description: <br>
GitHub Smart Code Digest monitors GitHub commits and pull requests, runs AI code review, creates visual digest cards, and publishes daily or weekly reports to Feishu Wiki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical leads, engineering managers, and open source maintainers use this skill to collect GitHub PR activity, review changes across correctness, security, maintainability, performance, and compliance, and publish code-quality digests to Feishu Wiki. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill publishes GitHub PR metadata, diff-derived review findings, file paths, and generated report images to Feishu Wiki. <br>
Mitigation: Install only for repositories intended for Wiki reporting, publish to a controlled Wiki space, and review reports before broad sharing. <br>
Risk: Scheduled daily or weekly runs can publish reports automatically after configuration. <br>
Mitigation: Enable schedules only after reviewing repository scope, Feishu destination, and expected publishing cadence. <br>
Risk: The workflow depends on GitHub and Feishu access credentials. <br>
Mitigation: Use restricted GitHub and Feishu credentials and review dependent skills before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/github-smart-code-digest) <br>
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen) <br>
- [README.md](artifact/README.md) <br>
- [Workflow definition](artifact/workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON intermediate data, generated image cards, and Feishu Wiki pages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review summaries, file-level findings, visual digest cards, and Wiki publishing output when GitHub and Feishu credentials are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, workflow.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
