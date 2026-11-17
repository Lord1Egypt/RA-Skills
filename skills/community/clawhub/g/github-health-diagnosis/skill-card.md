## Description:

GitHub Health Diagnosis analyzes a repository's issues, code quality, CI status, community activity, and security risk, then publishes a diagnostic report to Feishu Wiki.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical leads, maintainers, and due-diligence reviewers use this skill to assess GitHub repository health across code quality, issue activity, CI/CD status, community activity, and security risk. The skill is intended to generate a shareable Feishu Wiki report and diagnostic cards from a repository URL or owner/repo input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository assessment details, including security-review results, may be published to Feishu Wiki without an explicit publish confirmation or destination check.

Mitigation: Use this skill only when Wiki publication is acceptable, specify the intended Wiki space and parent location, and review or redact sensitive findings before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/github-health-diagnosis)
- [README.md](artifact/README.md)
- [workflow.json](artifact/workflow.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, Links, Structured data, Guidance]

**Output Format:** [Feishu Wiki page, diagnostic card images, and structured repository health scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an overall 0-100 score, dimension scores, issue summaries, recommendations, and Wiki/card links when publication succeeds.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
