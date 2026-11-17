## Description:

Reviews Japanese patent-application claims against Japanese Patent Act and JPO practice criteria, runs prior-art stability checks through configured patent-search integrations, and produces a structured HTML review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent professionals and agents use this skill to review Japanese patent claims from PDF, Word, or text submissions for legal compliance, claim structure, novelty and inventive-step risk, JPO practice concerns, foreign-filing adaptation, and protection strategy. It is intended to support drafting and review workflows, not replace formal legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent application content may be sent to the configured Zhihuiya MCP search service during novelty and inventive-step checks.

Mitigation: Confirm the MCP service configuration, authorization, and data-sharing expectations before using the skill with confidential patent materials.

Risk: The skill creates or replaces @skill_workspace/report.html as its output report.

Mitigation: Run it in an appropriate workspace and preserve any existing report file that should not be overwritten.

Risk: The generated patent review can inform drafting decisions but is not formal legal advice.

Mitigation: Have a qualified patent professional review conclusions and proposed claim amendments before filing or response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/jp-patent-claims-review)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [HTML report file plus concise text or Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a self-contained HTML report to @skill_workspace/report.html when the required patent-search MCP tools are configured.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
