## Description:

Create, modify, generate, and deploy websites, web apps, dashboards, SaaS products, internal tools, interactive web pages, Weixin mini programs, and games on the Baidu Medo platform using natural-language instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seiriosplus](https://clawhub.ai/user/seiriosplus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, iterate on, inspect, generate, and publish Medo-hosted web products from natural-language requirements. It is intended for websites, web apps, dashboards, SaaS products, internal tools, landing pages, interactive pages, Weixin mini programs, and browser games.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the Medo API key and project instructions to any configured API host if MEDO_BASE_URL or --base-url is changed.

Mitigation: Use a temporary or narrowly scoped Medo API key and avoid overriding the default API host unless the destination is fully trusted.

Risk: The skill documentation suggests weak key storage patterns and publishing can make generated apps publicly available.

Mitigation: Do not store the key in the skill directory .env file, review generated work before publishing, and publish only when public access is intended.

## Reference(s):

- [Medo official website](https://www.medo.dev)
- [ClawHub skill page](https://clawhub.ai/seiriosplus/skills/medo-app-builder)
- [Publisher profile](https://clawhub.ai/user/seiriosplus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and MEDO_API_KEY; can create and publish public Medo applications through the packaged CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
