## Description:

Assesses a proposed patent filing from a technical disclosure, patent number, or technical description across legal patentability, technical quality, market value, and strategic fit, producing a structured visual HTML report with recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent practitioners, R&D teams, and intellectual-property teams use this skill to decide whether a technical disclosure is ready for patent filing and what legal, technical, market, or portfolio issues need attention first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent-related queries may be sent through configured MCP or search services.

Mitigation: Use approved services for sensitive matters and avoid submitting confidential inventions unless the data path is acceptable.

Risk: Generated HTML reports can load third-party JavaScript.

Mitigation: Prefer an offline or bundled chart library when handling confidential inventions.

Risk: Generated reports may insert user-provided patent text into HTML without clear escaping guidance.

Mitigation: Require HTML escaping or sanitization before viewing generated reports in a browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-pre-filing-assessment)
- [PatSnap open platform](https://open.zhihuiya.com/)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, HTML, API Calls, Guidance]

**Output Format:** [Markdown guidance and structured HTML report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include patent claim element tables, comparison matrices, score summaries, visual report sections, and recommended filing actions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
