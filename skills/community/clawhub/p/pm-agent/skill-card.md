## Description:

PM Agent helps AI coding assistants critique PRDs, diagnose SaaS metrics, plan roadmaps, run discovery, coach PM career growth, and pressure-test AI product decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[digidai](https://clawhub.ai/user/digidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, product managers, and product leads use this skill inside AI coding tools to produce and review product-management work such as PRDs, roadmaps, discovery plans, SaaS diagnostics, competitive analysis, and career coaching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing outside ClawHub with the unpinned npx example could fetch an unintended source revision.

Mitigation: Prefer the ClawHub install path or use a pinned, reviewed source revision for non-ClawHub installation.

Risk: Generated templates may include an attribution footer that is not suitable for every external document.

Mitigation: Review generated PRDs, roadmaps, scorecards, and similar artifacts before sharing and remove or retain attribution according to the intended audience.

Risk: Product recommendations and SaaS diagnostics can be misleading if the input metrics, assumptions, or context are incomplete.

Mitigation: Validate key assumptions, metric definitions, baselines, and tradeoffs before relying on generated product decisions.

## Reference(s):

- [PM Agent ClawHub page](https://clawhub.ai/digidai/skills/pm-agent)
- [README](artifact/README.md)
- [Starter Prompts](artifact/STARTER-PROMPTS.md)
- [PRD Review Example](artifact/examples/prd-review.md)
- [SaaS Health Diagnostic Example](artifact/examples/saas-health-diagnostic.md)
- [Director Coaching Example](artifact/examples/director-coaching.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, analysis]

**Output Format:** [Markdown with structured product artifacts, concise bullet lists, and occasional plain-text prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include labeled assumptions, explicit tradeoffs, recommended next steps, and template attribution footers.]

## Skill Version(s):

1.3.1 (source: server release evidence; package.json lists 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
