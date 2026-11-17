## Description:

Fetches local Chinese government procurement notices from Beijing Zhongjian Yunzhi and Hunan Government Procurement sources, filters them by keywords, enriches matching records, and generates Excel reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpengle](https://clawhub.ai/user/zhangpengle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business-development teams use this skill to monitor local Chinese government procurement opportunities, filter notices by configured keywords, and produce Excel reports with buyer, agency, budget, timing, match, and recommendation fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live procurement credentials, which can expose account secrets if passed on the command line or stored in shared project files.

Mitigation: Avoid passing secrets on the command line; prefer temporary environment variables or a secret store, keep any .env file outside shared directories with owner-only permissions, and rotate credentials after use.

Risk: Reports generated from HTTP sources may be modified in transit.

Mitigation: Treat generated reports as untrusted until important opportunities are verified against the official source pages or another trusted record.

Risk: Procurement credentials are sent to the configured network path during authenticated collection.

Mitigation: Install and run the skill only in an environment where exposing those credentials to the configured procurement endpoint and network path is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangpengle/skills/goverment-bidding-fetcher)
- [Beijing Zhongjian Yunzhi procurement platform](http://zbcg-bjzc.zhongcy.com)
- [Hunan Government Procurement notices](http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Console text and Excel workbook (.xlsx)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes procurement results into source-specific Excel sheets; credential setup may write a local .env file.]

## Skill Version(s):

0.1.10 (source: ClawHub release evidence; pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
