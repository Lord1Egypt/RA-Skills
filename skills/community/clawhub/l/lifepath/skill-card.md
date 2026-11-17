## Description:

AI Life Simulator - Experience infinite lives year by year. Multiplayer intersections, dynasty mode, challenges, and Moltbook integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezbreadsniper](https://clawhub.ai/user/ezbreadsniper)

### License/Terms of Use:

MIT

## Use Case:

External agents and developers use LifePath to run an AI-powered life simulation backend, play complete year-by-year life stories through API or Telegram flows, and optionally share completed lives to Moltbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports serious security and privacy flaws before this backend should be installed or hosted as a public or shared service.

Mitigation: Do not run as a public or shared service until the security guidance is addressed and the service is reviewed after fixes.

Risk: Security evidence reports exposed Gemini keys.

Mitigation: Remove exposed keys from the package, rotate them, and require fresh secrets through the deployment environment.

Risk: Security evidence calls out weak database setup, missing authentication or ownership checks, permissive CORS or bind settings, and external posting risk.

Mitigation: Use a strong unique least-privilege database role, add authentication and ownership checks to life and Moltbook routes, restrict CORS and bind addresses, and require user preview and confirmation before posting externally.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ezbreadsniper/skills/lifepath)
- [LifePath README](README.md)
- [LifePath installation guide](INSTALL.md)
- [Moltbook semantic-trench community](https://moltbook.com/m/semantic-trench)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API examples, configuration values, and generated narrative text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, PostgreSQL, GEMINI_API_KEY, and DATABASE_URL; optional integrations use Telegram, Banana.dev, Moltbook, and Bankr-related settings.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
