## Description:

Helps agents create, modify, generate, and deploy apps and other content on Baidu Miaoda from natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seiriosplus](https://clawhub.ai/user/seiriosplus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Miaoda users can have an agent create and refine websites, mobile apps, and content, download generated files, and deploy apps when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: App generation can consume paid Miaoda credits.

Mitigation: Get human confirmation before generating an app and review expected account charges.

Risk: Publishing may make an app publicly available in production.

Mitigation: Publish only after an explicit user request and human confirmation; review the target and app before deployment.

Risk: The skill uses a Miaoda API key with access to the user's projects.

Mitigation: Store the API key in a secure environment mechanism, not a skill-directory .env file.

## Reference(s):

- [Miaoda official website](https://www.miaoda.cn)
- [Miaoda App Builder release on ClawHub](https://clawhub.ai/seiriosplus/skills/miaoda-app-builder)
- [ClawHub publisher profile](https://clawhub.ai/user/seiriosplus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Text or Markdown with app links and command results; downloadable source code and task files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [App generation and publishing use the user's Miaoda account; publishing is a separate, explicitly requested step.]

## Skill Version(s):

1.0.15 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
