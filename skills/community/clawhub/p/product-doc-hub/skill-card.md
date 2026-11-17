## Description:

Product Doc Hub gives AI product teams reusable PRD, product brief, experience validation framework, and configurable API console templates for product planning, handoff, demos, and API debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ildar981105-create](https://clawhub.ai/user/ildar981105-create)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, designers, and engineers use this skill to adapt product documentation templates and configure a lightweight API console for planning, stakeholder handoff, investor or team demos, and API debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API console assets include credential, telemetry, and live-API patterns that may be unsafe if reused as a production console without review.

Mitigation: Treat the API page as a mockup, remove or mask demo keys, remove credential and telemetry endpoints from defaults, and add sandbox-only guidance before reuse.

Risk: Mutating API requests could be sent from the console without enough safeguards.

Mitigation: Add explicit sandbox guidance and user confirmations for mutating requests before connecting the console to real services.

Risk: Reported DOM XSS and key-generation issues could matter if the assets are hosted on a real origin.

Mitigation: Fix those issues before hosting the console on a real origin or exposing it to real users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ildar981105-create/skills/product-doc-hub)
- [SKILL.md](artifact/SKILL.md)
- [API console configuration template](artifact/assets/api-console-config.js)
- [API console HTML template](artifact/assets/api.html)
- [PRD HTML template](artifact/assets/prd.html)
- [Product brief HTML template](artifact/assets/product-brief.html)
- [Experience framework HTML template](artifact/assets/experience-framework.html)
- [Nielsen Norman Group usability testing reference](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown guidance with HTML and JavaScript configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable HTML templates and a JavaScript API console configuration pattern.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
