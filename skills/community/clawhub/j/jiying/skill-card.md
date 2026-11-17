## Description:

Jiying is a multi-agent knowledge-work orchestration skill that applies policy checks, trusted execution envelopes, audit trails, and quality gates to make AI-assisted work more verifiable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vane1981](https://clawhub.ai/user/vane1981)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and knowledge-work teams use this skill to install and run Jiying for planning, research, creation, review, policy checks, audit logging, and export across a multi-agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path may execute mutable external code.

Mitigation: Audit the referenced package or repository before use, prefer a pinned release or commit, and run the skill in an isolated environment.

Risk: The workflow may handle sensitive API keys, model inputs, and audit data.

Mitigation: Use narrowly scoped credentials, avoid sensitive business data until logging and DeepSeek data flows are reviewed, and rotate keys after testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vane1981/skills/jiying)
- [Project portfolio](https://vane1981-2011.github.io/jiying/portfolio/)
- [Review report](https://vane1981-2011.github.io/jiying/portfolio/稽影系列_参赛作品_复核报告.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
