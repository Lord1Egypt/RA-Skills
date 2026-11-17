## Description:

Downloads complete Hong Kong listed-company financial reports from Eastmoney, 10jqka, and HKEX, prioritizing full reports over earnings announcements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance analysts use this skill to find and optionally download annual reports, interim reports, quarterly announcements, prospectuses, and a manifest for Hong Kong-listed companies by stock code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe input validation can allow downloaded files to be written outside the intended archive.

Mitigation: Restrict stock codes to numeric Hong Kong symbols and verify resolved output paths remain inside the archive before writing files.

Risk: PDF downloads can fetch unexpected URLs or oversized files.

Mitigation: Allowlist expected PDF hosts and enforce download size limits before using the --pdf option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/hk-financial-downloader)
- [Eastmoney announcements](https://data.eastmoney.com/notices/)
- [10jqka Hong Kong stock news](https://stockpage.10jqka.com.cn/HK{code}/news/)
- [HKEXnews listed company information](https://www1.hkexnews.hk/listedcompany/listedinfo/index_c.htm)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with bash examples; downloaded PDF files and manifest JSON when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and network access to the configured financial disclosure sources]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
