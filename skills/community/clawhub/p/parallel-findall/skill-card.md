## Description:

Discover entities matching a natural-language description through the Parallel FindAll API and return structured lists rather than webpages or prose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normallygaussian](https://clawhub.ai/user/normallygaussian)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research analysts use this skill to ask an agent for enumerable entities such as companies, people, products, or papers that match natural-language criteria. It helps the agent run Parallel FindAll, manage result limits and generator tiers, and relay structured matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command examples can become command-injection risks if an agent inserts raw user objectives directly into a command string.

Mitigation: Use structured argument invocation or carefully escape user-provided objectives before calling parallel-cli.

Risk: Base generator results may include noisy entries such as empty URLs, query-echo names, or category placeholders.

Mitigation: Filter noisy matches before relaying results and prefer the core or pro generator when coverage or precision matters.

## Reference(s):

- [Parallel](https://parallel.ai)
- [Parallel API Documentation](https://docs.parallel.ai)
- [FindAll API Reference](https://docs.parallel.ai/api-reference/findall)
- [Parallel CLI Integration](https://docs.parallel.ai/integrations/cli)
- [ClawHub Skill Page](https://clawhub.ai/normallygaussian/skills/parallel-findall)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and structured JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to preserve FindAll run IDs, filter noisy matches, and group large result sets for easier review.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
