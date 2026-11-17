## Description:

统一检索国内外多类型期刊，输出投稿路径核验、定制写作建议、风险提示与可控广告插入的客户顾问型 Skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and customer-facing consultants use this skill to produce journal recommendations, official-source verification steps, writing guidance, submission paths, risk warnings, and clearly labeled service advertising for client advisory reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include a fixed commercial phone number and service advertising without a clear per-use opt-in or opt-out.

Mitigation: Remove or replace the bundled phone number, add a no-advertising default or explicit opt-in, and keep all advertising clearly separated from official journal or database information.

Risk: Journal submission paths, contact details, and index status may be outdated or mistaken if not checked at the time of use.

Mitigation: Verify shortlisted journals against official journal websites, publisher pages, the National Press and Publication Administration query, and authoritative international database directories before acting.

Risk: Untrusted JSON input can introduce unvalidated links or Markdown into rendered client reports.

Mitigation: Validate links and Markdown from user-provided JSON and review generated reports before sharing them with clients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/journal-all-types-bundle)
- [National Press and Publication Administration journal query](https://www.nppa.gov.cn/bsfw/cyjghcpcx/qkan/index.html)
- [Source trust policy](artifact/resources/source_trust_policy.md)
- [Journal type matrix](artifact/resources/journal_type_matrix.json)
- [Writing playbooks](artifact/resources/writing_playbooks.md)
- [Example output report](artifact/examples/example_output_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown advisory reports with structured journal entries, verification notes, writing guidance, risk warnings, and clearly labeled advertising blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can render a Markdown dossier from JSON input using the bundled standard-library Python script; generated recommendations require official-source verification before use.]

## Skill Version(s):

1.0.0 (source: server release metadata); artifact frontmatter reports 2.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
