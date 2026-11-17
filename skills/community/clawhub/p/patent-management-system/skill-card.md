## Description:

Builds a single-file HTML patent management system for synthetic biology and life science companies using PatSnap/智慧芽 patent data and workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Intellectual property teams and agent users use this skill to generate or update a patent management HTML system with patent assets, fee alerts, competitor tracking, FTO analysis, patent value evaluation, and novelty search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent searches and analysis may involve confidential product plans, unpublished invention details, or sensitive competitor strategy.

Mitigation: Use the PatSnap/智慧芽 integration only under organizational data-sharing approval and avoid submitting sensitive information unless permitted.

Risk: Generated HTML reports may overwrite or update existing local patent reports if filenames are reused.

Mitigation: Review generated filenames and version increments before writing or replacing local report files.

Risk: Without MCP authorization, live patent retrieval and database-backed conclusions are unavailable.

Mitigation: Complete PatSnap/智慧芽 MCP authorization before relying on live patent data; otherwise treat outputs as analysis framework guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-management-system)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [Eureka patent full-text link pattern](https://eureka.zhihuiya.com/view/#/fullText?patentId={patentId})

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and single-file HTML code or update instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML is expected to be UTF-8, browser-viewable, and written as a versioned patent_v{n}.html file.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
