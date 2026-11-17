## Description:

Generates, scaffolds, builds, and verifies a React + Vite + Hono commerce storefront from a short product brief, including catalog, cart, wishlist, checkout, admin, AI sales assistant, and EdgeOne Pages deployment files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwter](https://clawhub.ai/user/lwter)

### License/Terms of Use:

MIT

## Use Case:

Developers and ecommerce teams use this skill to turn a one-line product idea into a runnable storefront scaffold, then validate and build it before handoff or EdgeOne deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and edits a generated project and asks the agent to run npm commands.

Mitigation: Review generated files before public deployment, run the bundled validation gate, and run the project build in the target environment.

Risk: The scaffold includes payment and AI provider integration points with placeholder environment variables.

Mitigation: Keep payments in mock or test mode until production services are connected, and store live secrets only in a secret manager or deployment environment.

Risk: The generated storefront is scaffold-ready and demo-ready, but real payments, persistence, authentication, and order operations require production services.

Mitigation: Connect and verify production backends, webhook handling, order state, and hosted checkout before treating the site as production-ready.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lwter/skills/neway-commerce-os)
- [Architecture](references/architecture.md)
- [Commerce Flows](references/commerce-flows.md)
- [Deployment](references/deployment.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated project files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated projects include React and Vite source, Hono-style functions, EdgeOne configuration, validation output, and handoff notes.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
