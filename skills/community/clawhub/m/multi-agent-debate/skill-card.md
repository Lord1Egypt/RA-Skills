## Description:

Multi-Agent Debate helps agents verify facts, reduce hallucinations, and explore multiple viewpoints by generating independent answers, structured critiques, optional refinements, and consensus or verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simoncatbot](https://clawhub.ai/user/simoncatbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and teams use this skill to structure multi-agent debate for fact-checking, complex reasoning, trade-off analysis, and hallucination checks where independent critique improves answer quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The debate pattern can increase model usage and latency because it asks for multiple independent answers and critique rounds.

Mitigation: Use it for complex or high-accuracy tasks, and skip it for simple facts, purely creative work, or speed-critical requests.

Risk: A forced consensus may hide legitimate disagreement or produce misleading confidence.

Mitigation: Keep initial answers independent, require specific critiques, and preserve defensible disagreement when consensus is not warranted.

## Reference(s):

- [Detailed Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with reusable debate templates and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May increase latency and model usage because multiple independent answers and critique rounds are requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
