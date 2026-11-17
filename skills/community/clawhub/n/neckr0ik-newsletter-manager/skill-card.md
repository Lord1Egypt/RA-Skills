## Description:

Manage newsletter drafts with AI-generated content, local subscriber imports, scheduling state, simulated sending, and basic analytics for newsletter workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT

## Use Case:

External creators, newsletter operators, and developers use this skill to draft newsletter content, manage local subscriber records, schedule drafts, and inspect basic analytics during newsletter workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents newsletter delivery, scheduling, web curation, and analytics as operational capabilities even though the release evidence says these outputs should be treated as simulated.

Mitigation: Use the skill for local drafting and workflow experiments only until real provider integrations, explicit approval safeguards, and verified analytics are implemented.

Risk: The skill can store API keys and subscriber records locally while the authoritative security guidance flags weak safeguards for credentials and subscriber data.

Mitigation: Do not enter live API keys or import real subscriber lists unless storage, redaction, and permission controls are reviewed and fixed.

Risk: AI-generated newsletter content and curated links may be inaccurate, incomplete, or unsuitable for the intended audience.

Mitigation: Review generated content, links, and analytics claims before sending or publishing any newsletter material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-newsletter-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python examples; generated newsletter drafts are Markdown-like text and local operational records are JSON or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores drafts, subscriber records, analytics, and configuration locally; provider sending and analytics should be treated as simulated until real integrations are verified.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, claw.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
