## Description:

Free meme coin signal scanner. Aggregates DEXScreener, Pump.fun, GeckoTerminal, CoinGecko trending data. Scores tokens 0-100 with risk assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidadong2359](https://clawhub.ai/user/weidadong2359)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to scan meme-token market data from free public sources, score opportunities, and summarize risk signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can auto-start from broad terms and poll external services repeatedly.

Mitigation: Require explicit user opt-in before scanning and limit polling frequency, scope, and duration.

Risk: The security review says the skill stores signals temporarily and reports strong signals to an undefined creator.

Mitigation: Avoid creator reporting by default, disclose any reporting path, and keep retained signal data limited to the documented 24-hour window.

Risk: The security verdict is suspicious even though no code execution, credential theft, or destructive behavior was found.

Mitigation: Review before installing and deploy only where automatic crypto scans and third-party market API lookups are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidadong2359/skills/meme-signal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and structured signal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signal summaries include token identifiers, chain, score, risk label, market metrics, narrative tag, and reference URL when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
