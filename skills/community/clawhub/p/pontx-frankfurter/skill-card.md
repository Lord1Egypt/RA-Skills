## Description:

Maintain legacy Frankfurter v1 integrations through Pontx. Use for existing v1 applications, reproducible dated reference-rate work, or deciding whether new provider-aware work should move to pontx-frankfurter-v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to maintain existing Frankfurter v1 exchange-rate integrations through Pontx, prepare reproducible dated reference-rate requests, and decide when v2 migration is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward live exchange-rate retrieval through Pontx.

Mitigation: Preview requests first and execute live reads only when the user explicitly asks for retrieval.

Risk: Frankfurter v1 behavior may differ from v2 or from current catalog metadata.

Mitigation: Inspect the current Pontx contract before coding and stop if product guidance conflicts with the live contract.

Risk: Reference exchange rates can be mistaken for guaranteed execution or settlement prices.

Mitigation: Describe values as reference rates and perform amount conversion with decimal-capable arithmetic in application code.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline shell commands and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Pontx CLI preview or call commands when the user asks for live retrieval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
