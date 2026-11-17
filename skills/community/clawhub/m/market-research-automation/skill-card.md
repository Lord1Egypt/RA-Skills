## Description:

Market Research Automation helps agents produce market sizing reports, competitor comparisons, and survey questionnaires for product validation and user research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, product managers, and market researchers use this skill to draft TAM/SAM/SOM reports, competitor matrices, and survey instruments before product launch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can appear to perform live social-media or competitor research even though the security evidence describes it as a local mock report generator.

Mitigation: Treat generated reports as templates or mock examples unless real source data is independently supplied and verified.

Risk: The documented dependency install may add unnecessary packages for the current local generator behavior.

Mitigation: Install and run the skill in an isolated environment and only add dependencies that are required for the intended workflow.

## Reference(s):

- [Market Research Methodology Reference](references/methodology.md)
- [X/Twitter API](https://developer.x.com/en/docs/x-api)
- [Google Trends](https://www.google.com/trends/)
- [Full Market Research Agent Use Case](https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/market-research-product-factory.md)
- [ClawHub Skill Release](https://clawhub.ai/openlark/skills/market-research-automation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports and questionnaires, printed to the terminal or saved as Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may contain mock examples or data-unavailable markers unless the user supplies and verifies real data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
