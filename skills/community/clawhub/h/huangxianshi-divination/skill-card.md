## Description:

黄仙师灵签抽签与解签。用户说“聊签/求签/抽一签/来一签/解签/全部解签”时使用。随机抽取1签并返回吉凶、签号、签题、签诗、典故全文；支持按方向解签或全部解签。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nzleo](https://clawhub.ai/user/nzleo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to draw a Huangxianshi fortune lot and request a concise explanation by topic such as career, wealth, relationships, health, yearly outlook, story, or all available aspects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The undocumented sunrise helper contacts wttr.in over plaintext HTTP, uses hardcoded Shanghai timing, and may wait before running a draw.

Mitigation: Review or disable that helper before installation unless the network request, location assumption, and wait behavior are acceptable; prefer HTTPS, response validation, documentation, or removal.

Risk: Fortune-lot explanations may be mistaken for high-confidence professional advice.

Mitigation: Use the skill as reflective or entertainment-oriented guidance and avoid treating outputs as medical, legal, financial, or other high-stakes determinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nzleo/skills/huangxianshi-divination)
- [Publisher profile](https://clawhub.ai/user/nzleo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise Chinese text cards, JSON from CLI commands when requested, and shell command examples in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The draw flow can save the most recent draw locally so later explanation requests can default to the previous lot.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
