## Description:

根据用户描述的技术问题检索专利，按解决思路归类，并汇总代表性专利与关键做法供研发参考。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

研发人员和工程师可描述遇到的技术瓶颈，检索专利中公开的解决思路，并将代表性专利、关键做法和参数整理成参考表。结果用于研发参考，不判断可专利性或提供法律结论。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key may be exposed, and credentials remain saved locally.

Mitigation: Supply the key securely, use a limited-spend key, protect local credential storage, and agree on spending limits.

Risk: Crafted patent numbers may enable file access outside the cache.

Mitigation: Run the skill with isolated filesystem access and prefer a version that confines cache paths and restricts authenticated requests to an approved HTTPS origin.

Risk: Confidential invention details could be disclosed in patent-search queries.

Mitigation: Exclude confidential invention details from queries.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/patent-solution-finder)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Search workflow](artifact/references/search-workflow.md)
- [Query construction](artifact/references/query-construction.md)
- [API reference](artifact/references/api-reference.md)
- [Known pitfalls](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, CSV, Guidance]

**Output Format:** [UTF-8 CSV with BOM and a concise conversational summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The table groups representative patents by solution approach and records key measures, parameters, and source references; it is a research aid, not a legal opinion.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
