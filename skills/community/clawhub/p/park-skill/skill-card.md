## Description:

Park Skill helps industrial, technology, and business park teams answer bilingual questions about park information, recruitment policies, enterprise services, operations, and dashboard statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Park operators, leasing teams, property managers, and enterprise service staff use this skill to answer park operations questions, explain leasing and incentive policies, guide enterprise services, and summarize operational metrics in Chinese or English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled park, policy, rent, and operating figures appear to be static sample data and may not match a deploying organization's actual park.

Mitigation: Replace config/park-config.yaml with current approved park data before production use, and have policy, rent, and service figures reviewed by the responsible business owner.

Risk: Broad activation examples may cause the skill to answer adjacent real estate, policy, or enterprise service questions when the user did not clearly ask for park operations help.

Mitigation: Tighten activation examples and routing rules so the skill is invoked only for explicit park operations, leasing, enterprise service, property, or dashboard requests.

Risk: The skill can present compliance, tax incentive, environmental, and safety information that users may treat as authoritative guidance.

Mitigation: Label responses that involve policy or compliance as informational and require review against current local rules and park-specific procedures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/park-skill)
- [Park Skill README](artifact/README.md)
- [Park Configuration](artifact/config/park-config.yaml)
- [Example Queries](artifact/examples/example-query.md)
- [Example Outputs](artifact/examples/example-output.md)
- [Skill Homepage](https://xiaping.coze.site)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Bilingual Markdown responses, Markdown tables, structured JSON, and report-style summaries; artifact documentation also describes Excel, PDF, and PPT export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports zh-CN and en-US responses using static configuration and locale files.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact files list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
