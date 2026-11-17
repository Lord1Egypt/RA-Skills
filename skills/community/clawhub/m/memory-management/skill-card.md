## Description:

Manages authorized HOT/WARM/COLD project memory for initialization, review, consolidation, archival, and subject erasure while preserving registry ownership and privacy controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and project operators use this skill to manage persistent project context across agent sessions, including memory initialization, lookup, consolidation, archival, and authorized erasure. It is intended for local working memory and does not replace canonical registry ownership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local project memory can include sensitive project, personal, credential, or production data.

Mitigation: Use the skill only in repositories where persistent project context is acceptable, keep runtime memory out of normal commits, and avoid seeding raw personal data, credentials, or production exports.

Risk: Writes, purges, and cross-project comparisons can affect local memory records beyond the intended scope.

Mitigation: Confirm paths and subject scope before persistent writes or purges, use dry-run review when scope is ambiguous, and require explicit authorization for destructive or privacy-sensitive actions.

Risk: Cached summaries or lower-authority memory notes may be stale or conflict with canonical registry facts.

Mitigation: Treat cached memory as retrieval support only, preserve conflicts, and route canonical fact changes through the owning registry.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/memory-management)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Consolidation Pass](references/consolidation-pass.md)
- [Memory Management Examples](references/examples.md)
- [Erasure Operation Log Template](references/gdpr-purge-log-template.md)
- [Glossary Template](references/glossary-template.md)
- [Hot Cache Template](references/hot-cache-template.md)
- [Promotion and Demotion Rules](references/promotion-demotion-rules.md)
- [Update Triggers and Cross-Skill Integration](references/update-triggers-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline commands, file path summaries, templates, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify authorized local memory files, archives, indexes, and tombstone records after explicit user authorization.]

## Skill Version(s):

19.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
