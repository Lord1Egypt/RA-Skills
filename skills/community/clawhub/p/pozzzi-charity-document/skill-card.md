## Description:

噗滋（pozzzi）慈善文书助手帮助中小型 NGO 生成合同协议、会议纪要、公函、感谢信和工作计划，并通过固定合同条款降低关键条款被模型改写的风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309)

### License/Terms of Use:

MIT-0

## Use Case:

External NGO operators and administrative staff use this skill to draft routine Chinese-language administrative documents, including agreements, meeting minutes, official letters, thank-you letters, and work plans. The skill is suited for draft preparation and requires human legal or administrative review before real-world use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive contract, meeting, donor, or official-correspondence fields through the configured model provider.

Mitigation: Treat all document fields as potentially model-bound, avoid entering personal data unless necessary, and prefer roles or placeholders over real names.

Risk: Generated contracts or official documents may contain incomplete, incorrect, or non-final language.

Mitigation: Require human legal or administrative review before signing, sending, filing, or publishing generated drafts.

Risk: Evidence security review reports that privacy and prompt-safety controls are narrower than the skill's assurances for sensitive administrative and contract content.

Mitigation: Review the skill before installation for real administrative use, keep sensitive inputs minimal, and validate outputs against organizational policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aikawabigsky309/skills/pozzzi-charity-document)
- [Ministry of Civil Affairs charity policy reference](https://www.mca.gov.cn/article/yw/hjzcbz/)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown document drafts with validation warnings and generation metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document type controls template, tone, token budget, and fixed-clause handling; generated drafts include AI-use and review disclaimers.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
