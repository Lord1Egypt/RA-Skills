## Description:

Mirofish helps agents turn seed material such as news, policy drafts, financial signals, or story material into offline MiroFish-style prediction workflows with ontology sketches, simulation plans, forecast briefs, and interview questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y3519712124-ui](https://clawhub.ai/user/y3519712124-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to transform scenario seed material into a structured offline prediction workflow. It is best suited for forecast-style planning where the answer should preserve causal structure, competing incentives, branch drivers, uncertainty, and interview prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional live-backend path can upload user files and inspect backend secret configuration.

Mitigation: Use offline mode by default, confirm the backend URL before live execution, avoid uploading confidential seed files unless the destination is trusted, and do not expose .env secret values.

Risk: Reset, delete, force-regenerate, or log-clearing operations in the live-backend path can alter or remove backend state.

Mitigation: Require explicit user confirmation before reset, delete, force, or log-clearing operations and preserve useful partial report output before retrying generation.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/y3519712124-ui/MiroFish-skills/tree/main/mirofish)
- [ClawHub skill page](https://clawhub.ai/y3519712124-ui/skills/mirofish)
- [Offline Playbook](references/offline-playbook.md)
- [Output Patterns](references/output-patterns.md)
- [Workflow Map](references/workflow-map.md)
- [API Surface](references/api-surface.md)
- [Runtime Contract](references/runtime-contract.md)
- [Worked Example](references/worked-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown with structured sections and optional inline shell commands for explicitly requested live-backend use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline outputs should include at least three branches, five interview questions, one revision pass, and clear separation of facts, inferences, and uncertainty.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
