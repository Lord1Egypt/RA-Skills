## Description:

Jd Search helps agents run keyword, category, price-range, and paginated product searches against JD Gongcai Cloud, returning table, JSON, or CSV results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangr19](https://clawhub.ai/user/zhangr19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents in JD internal environments use this skill to search Gongcai Cloud product data, filter by category or price, paginate results, and choose table, JSON, or CSV output for downstream review or automation.

### Deployment Geography for Use:

Global, limited to JD internal network environments where the required service and executable are available.

## Known Risks and Mitigations:

Risk: The skill depends on a JD internal search service and a jd-search executable that may not be available in all environments.

Mitigation: Install only in the intended JD internal environment and verify the executable with the publisher before use.

Risk: Search terms may be visible to internal network infrastructure, especially where HTTPS or authenticated transport is not confirmed.

Mitigation: Avoid sensitive query terms unless the deployment has acceptable transport and access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangr19/skills/jd-search)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, CSV]

**Output Format:** [Markdown guidance with CLI examples; command output as table, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports keyword, category ID, page, page size, price range, output format, and category display options.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
