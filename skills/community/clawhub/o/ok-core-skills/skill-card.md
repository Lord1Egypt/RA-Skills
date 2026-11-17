## Description:

OK Core Skill enables agents to automate OK.com classifieds workflows, including searching and browsing listings, viewing listing details, managing favorites and posted ads, checking login state, and switching locales across supported countries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winterw](https://clawhub.ai/user/winterw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to search OK.com classifieds, inspect listing details, manage saved favorites and posted ads, and navigate OK.com country and city locales through a CLI-driven browser automation workflow.

### Deployment Geography for Use:

Singapore, USA, Canada, Japan, UAE, Australia, UK, Hong Kong, Malaysia, and New Zealand

## Known Risks and Mitigations:

Risk: The skill exposes sensitive browser and account control for OK.com automation.

Mitigation: Review before installing, use a separate browser profile, and close the bridge and debug-enabled Chrome after use.

Risk: Login, favorites, and posted-ad workflows can affect a live OK.com account.

Mitigation: Prefer manual browser or OAuth login over giving the agent a password, and confirm the exact favorite or post before modifying or deleting it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/winterw/skills/ok-core-skills)
- [Publisher profile](https://clawhub.ai/user/winterw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands return structured JSON for listings, locales, authentication state, favorites, and posted-ad operations.]

## Skill Version(s):

0.0.5 (source: ClawHub release evidence; artifact frontmatter says 1.0.0 and pyproject.toml says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
