## Description:

LLM hallucination detector with dual strategy (UQLM + rule-based fallback). Scores any AI output's confidence and flags potential hallucination risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li8476295-bot](https://clawhub.ai/user/li8476295-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check AI-generated text for hallucination risk before critical operations such as code execution, SQL, or external sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external uqlm package and its dependencies are the main trust boundary.

Mitigation: Install in a virtual environment or container, pin dependency versions, and avoid running with sensitive credentials or broad filesystem access.

Risk: Hallucination confidence scores and rule-based fallback results may miss or misclassify risky content.

Mitigation: Use results as a screening signal and keep human review for critical code, SQL, or external communications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li8476295-bot/skills/hallucination-check)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON containing confidence, risk level, and suggestion fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports threshold-based risk classification and a rule-based fallback when UQLM dependencies are unavailable.]

## Skill Version(s):

1.0.0 (source: clawhub.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
