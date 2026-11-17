## Description:

校验文本中的法律引用，抽取法规、法条、案例和案号，并通过权威来源比对语义一致性与法规时效性，输出准确、时效风险、语义不一致或未命中的判定。

This skill is ready for commercial/non-commercial use.

## Publisher:

[doudoudou12138-design](https://clawhub.ai/user/doudoudou12138-design)

### License/Terms of Use:

MIT-0

## Use Case:

Legal professionals, compliance reviewers, and developers use this skill to check whether legal citations in formal Chinese legal text match authoritative source content and remain valid. It supports review of cited regulations, statutes, cases, and case numbers before legal text is finalized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential or privileged legal text may be sent to the disclosed chineselaw.com API.

Mitigation: Use the skill only when that service is approved for the matter, and avoid privileged or highly confidential material unless approval is explicit.

Risk: API keys or generated request and response files may expose secrets or sensitive legal text.

Mitigation: Keep YUANDIAN_API_KEY out of chats and source control, and delete or protect body.json and response.json after use.

Risk: Failed or incomplete API responses could otherwise lead to unsupported legal claims.

Mitigation: Do not fabricate legal authority when the API fails or returns no authoritative source content; report the failure or missing result instead.

## Reference(s):

- [ChineseLaw hall_detect API endpoint](https://open.chineselaw.com/open/hall_detect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown table with concise text and API-backed citation-check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses YUANDIAN_API_KEY and may create local body.json and response.json files during citation checks.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
