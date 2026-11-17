## Description:

Autonomous verification engine that deconstructs claims, evaluates source credibility, and identifies contradictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mustafa-cuda-dev](https://clawhub.ai/user/mustafa-cuda-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to check factual claims against live web search results, summarize supporting evidence, and surface possible contradictions with confidence scoring and citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User claims are sent to DuckDuckGo-backed search during verification.

Mitigation: Avoid submitting sensitive or confidential claims unless external search disclosure is acceptable.

Risk: Confidence scores and source credibility are heuristic and may overstate verification quality.

Mitigation: Treat results as research assistance and review cited sources before relying on the report for decisions.

Risk: Security guidance notes that a dependency pin should be updated and source hostname validation should be improved.

Mitigation: Prefer a release that updates requests and validates source hostnames before deployment in stricter environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mustafa-cuda-dev/skills/omni-research-verifier)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an executive summary, evidence table, contradictions, citations, confidence score, and processing metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
