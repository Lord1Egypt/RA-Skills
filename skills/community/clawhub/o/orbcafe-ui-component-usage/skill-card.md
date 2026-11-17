## Description:

Route ORBCAFE UI requests to the correct module skill and enforce official examples-based integration baseline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenruiyang](https://clawhub.ai/user/shenruiyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to classify ORBCAFE UI requests, choose the right module skill, and produce minimal runnable integration guidance using public ORBCAFE APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest npm dependencies and project startup commands that affect a local application environment.

Mitigation: Review the listed ORBCAFE UI and peer dependencies before installing them, and run commands in the intended project workspace.

Risk: Broad routing keywords can select the wrong ORBCAFE module when a request is ambiguous.

Mitigation: Confirm the selected module against the routing map and module contracts before applying generated code.

Risk: Generated integration code can fail when it uses non-public imports or unsafe Next.js hydration patterns.

Mitigation: Use only the public `orbcafe-ui` entry point and verify the integration with the provided startup, interaction, persistence, and hydration checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenruiyang/skills/orbcafe-ui-component-usage)
- [Skill routing map](references/skill-routing-map.md)
- [AI module contracts](references/module-contracts.md)
- [Machine-readable module contracts](references/module-contracts.json)
- [Integration baseline](references/integration-baseline.md)
- [Public export index](references/public-export-index.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and verification checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes module decision, paste-ready public imports, data shape, verification steps, and troubleshooting steps.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
