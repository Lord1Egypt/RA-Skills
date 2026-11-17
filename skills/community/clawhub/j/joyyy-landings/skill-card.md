## Description:

Returns a landing URL for rapid interactive prototypes, including game engines, simulations, visual analytics, and investor-ready demos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vziatkov](https://clawhub.ai/user/vziatkov)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, AI teams, and product teams use this skill when they need an agent-callable portfolio entry that returns live interactive demo links for prototypes, investor demos, simulations, and visual explainers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may trigger on broad portfolio, demo, investor, or prototype wording and return this creator's demo links when a user expected a different portfolio.

Mitigation: Confirm the user is asking for vziatkov's interactive prototype portfolio or demos before invoking or sharing the returned links.

Risk: Optional screenshot and demo-video utilities install and run third-party Python tooling.

Mitigation: Run those utilities only in a clean virtual environment with reviewed dependencies before publishing generated media.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vziatkov/skills/joyyy-landings)
- [Landing Demo](https://vziatkov.github.io/neuro/landing-with-art-cards.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text containing one or more demo URLs and a concise reply phrase.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API calls, credentials, or backend services are required for normal skill use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
