## Description:

Helps analyze cooperation failures by modeling payoffs, identifying a prisoner's dilemma, and evaluating structural ways to make cooperation rational.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to diagnose cooperation failures in negotiations, partnerships, markets, and shared-resource problems. It structures the analysis around a payoff matrix and helps evaluate whether repetition, reputation, enforcement, or a changed game structure can support cooperation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect payoff model or game classification can lead to ineffective cooperation advice.

Mitigation: Fill in all four payoffs, verify the Prisoner's Dilemma ordering, and rule out other game types before recommending an escape.

Risk: Recording real-use examples may expose confidential details.

Mitigation: Omit confidential details when documenting examples.

## Reference(s):

- [Primary sources and further reading](artifact/references/sources.md)
- [Flood, Some Experimental Games](https://doi.org/10.1287/mnsc.5.1.5)
- [Nash, Equilibrium Points in n-Person Games](https://doi.org/10.1073/pnas.36.1.48)
- [Prisoner's Dilemma skill page](https://clawhub.ai/deciqai/skills/prisoners-dilemma)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Structured Markdown game diagnosis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes players, payoff matrix, game classification, dominant strategies, equilibrium, and escape options with a post-change test.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
