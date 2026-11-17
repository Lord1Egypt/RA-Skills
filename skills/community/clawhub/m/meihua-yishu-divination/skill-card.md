## Description:

A Meihua Yishu divination skill that creates hexagrams from time, numbers, or Chinese text, then provides structured interpretation using body-use five-element relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to perform Meihua Yishu divination for entertainment and self-exploration, using time, numeric, or text-based inputs. The skill is suited to agents that need to show the calculation process, interpret the resulting hexagrams, and provide non-professional action suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically read shared fortune-telling preferences from another skill memory file without fresh user consent or clear field limits.

Mitigation: Before deployment, restrict cross-skill memory reads to explicit preference fields and ask the user before using shared memory.

Risk: Divination output may be mistaken for professional advice or deterministic prediction.

Mitigation: Keep the skill disclaimer and require outputs to frame readings as entertainment and self-exploration, not medical, legal, or financial advice.

## Reference(s):

- [Meihua Yishu calculation rules](artifact/references/calculation-rules.md)
- [Meihua Yishu interpretation guide](artifact/references/interpretation-guide.md)
- [Project homepage](https://github.com/eamanc-lab/fortune-telling-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with tables, calculations, interpretive prose, and action suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include a disclaimer that readings are for entertainment and self-exploration, not professional advice.]

## Skill Version(s):

1.0.0 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
