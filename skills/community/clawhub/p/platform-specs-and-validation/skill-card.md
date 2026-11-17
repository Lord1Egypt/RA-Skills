## Description:

Platform specs and publish validation helps agents map per-platform WoopSocial requirements, resolve target-specific fields, enforce media rules, and run the validate-before-publish loop before atomic post creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and social publishing teams use this skill to prepare multi-platform WoopSocial posts by mapping required fields, checking media constraints, resolving account-specific values, and validating before publish. It supports publish readiness and validation repair; creative quality, compliance truthfulness, privacy intent, and performance claims remain human responsibilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A post may publish to the wrong accounts or with unintended privacy, disclosure, or compliance settings.

Mitigation: Review selected accounts, privacy settings, branded-content declarations, made-for-kids declarations, and validation warnings before creating the post.

Risk: WoopSocial creates posts atomically and has no update endpoint, so a mistake may require delete and recreate while deliveries are still NOT_STARTED.

Mitigation: Run POST /posts/validate first, resolve all errors, review warnings, and treat delete-and-recreate actions as explicit human-reviewed changes.

Risk: Platform enums, limits, and media constraints can change over time.

Mitigation: Re-check the live WoopSocial OpenAPI contract or integration guide before relying on volatile platform-specific requirements.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/social-media-skills/skills/platform-specs-and-validation)
- [Scope, distinctions + connections](references/scope-and-connections.md)
- [The CHECK framework](references/the-check-framework.md)
- [Validation reference + two worked examples](references/validation-reference-and-recipes.md)
- [WoopSocial publish spec - per-platform matrices](references/woopsocial-publish-spec.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, API call plans]

**Output Format:** [Markdown guidance with field mappings, validation steps, and concise checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No hidden code, persistence, or unrelated access detected in security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
