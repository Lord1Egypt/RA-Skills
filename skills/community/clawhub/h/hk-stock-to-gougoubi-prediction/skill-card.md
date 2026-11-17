## Description:

Turn Hong Kong stock research into Gougoubi-ready prediction proposals with deterministic market wording, deadline selection, resolution rules, and tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Hong Kong stock or theme research into a single objectively resolvable Gougoubi prediction-market proposal with clear deadlines, rules, tags, and optional creation input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated market titles, deadlines, or resolution rules could be incorrect or misleading and may have public or financial consequences if submitted.

Mitigation: Review each generated proposal before allowing actual Gougoubi submission, and require explicit user intent before submitting through the UI or on-chain.

Risk: A proposal may depend on unclear earnings dates, unavailable sources, illiquid securities, subjective judgments, or non-public resolution data.

Mitigation: Apply the skill's market filters: use time-bounded, externally resolvable, single-thesis markets with public sources, and surface uncertainty when source availability or dates are unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasong/skills/hk-stock-to-gougoubi-prediction)
- [Gougoubi public proposal creation page](https://gougoubi.ai/premarket/proposals/create/public)
- [Tencent 00700 example](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, API calls, guidance]

**Output Format:** [Markdown response with structured JSON payload fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes analysis summary, chosen prediction, Gougoubi payload, minimal create input, optional create result, and warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
