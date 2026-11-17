## Description:

Create and manage Meta (Facebook and Instagram) ad campaigns, lead forms, audiences, pixels, product catalogs, and account connections through the Plai API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arsalan98m](https://clawhub.ai/user/arsalan98m)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect ad accounts and operate Meta advertising workflows through Plai, including campaign creation, reporting, budget and status updates, lead forms, audiences, pixels, media, and product catalogs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plai credentials and ad-account data are sent to an API endpoint controlled by the PLAI_BASE_URL environment variable.

Mitigation: Keep PLAI_BASE_URL unset or pinned to the legitimate Plai endpoint, avoid wrappers or CI jobs that can alter environment variables, and use a scoped, rotatable API key where possible.

Risk: The skill can create, activate, delete, and change budgets for advertising campaigns.

Mitigation: Review generated commands before execution and require explicit user confirmation before actions that spend budget, activate campaigns, delete campaigns, or modify live campaign settings.

Risk: OAuth connection links can connect Facebook, Instagram, or Google Ads accounts to Plai.

Mitigation: Share connection links directly with the user, let the user complete OAuth in their browser, and confirm the intended platform before generating a link.

## Reference(s):

- [Plai](https://plai.io)
- [Meta AI Ads on ClawHub](https://clawhub.ai/arsalan98m/skills/meta-ai-ads)
- [Plai public API endpoint](https://public.plai.io)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus PLAI_API_KEY and PLAI_USER_ID environment variables.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
