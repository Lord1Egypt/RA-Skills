## Description:

Mystilink Liuyao forms Liu Yao six-line hexagrams from six casts and supports readings with Mystilink Wiki method pages and Zhouyi chapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystilink-ai](https://clawhub.ai/user/mystilink-ai)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to cast and read Liu Yao hexagrams for one concrete matter at a time, using local casting output plus Mystilink Wiki method and classics references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch Mystilink Wiki reference pages, which may expose sensitive personal details if users include them in remote searches.

Mitigation: Avoid sensitive personal details in remote Wiki searches; use fixed page lookups or local references when privacy matters.

Risk: The skill runs a local Node casting script.

Mitigation: Install and run it only in environments where local Node execution is acceptable, and review the script before deployment.

Risk: Liu Yao readings can be mistaken for authoritative advice on consequential decisions.

Mitigation: Keep readings framed as interpretive guidance and avoid using them as the sole basis for financial, legal, medical, or safety-critical decisions.

## Reference(s):

- [Mystilink Liuyao Skill on ClawHub](https://clawhub.ai/mystilink-ai/skills/mystilink-liuyao-skill)
- [Server-resolved GitHub repository](https://github.com/mystilink-ai/mystilink-liuyao-skill)
- [Liuyao Skill Reference](references/overview.md)
- [Mystilink Liuyao Method Page](https://wiki.mystilink.com/api/v1/pages/liuyao.method.six-casts?locale=en)
- [Mystilink Ben-Zhi-Bian Rule Page](https://wiki.mystilink.com/api/v1/pages/liuyao.rule.ben-zhi-bian?locale=en)
- [Mystilink Yijing Classics Page](https://wiki.mystilink.com/api/v1/pages/shared.work.yijing.gua.01-qian?locale=zh-Hans)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API request examples, and JSON casting output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node casting can emit deterministic JSON when seed or throws are provided; wiki lookups may require network access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
