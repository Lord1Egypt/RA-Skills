## Description: <br>
Manages SEO/GEO project memory, including hot-cache, active work, archive tiers, wiki indexes, and privacy cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and SEO teams use this skill to preserve project context across sessions, manage memory tiers, update wiki-derived memory views, and clean up stored personal data when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create durable local project memory that may include sensitive business context or personal data. <br>
Mitigation: Store only necessary information, avoid secrets and unnecessary personal data, and use the documented purge flow when deletion is required. <br>
Risk: Archive, restore, wiki, and purge operations can change or remove local memory files. <br>
Mitigation: Review proposed changes before applying them, confirm destructive operations explicitly, and keep audit records for privacy-related purges. <br>
Risk: Automatic hook behavior may refresh derived memory surfaces or load hot-cache context across sessions. <br>
Mitigation: Review hook configuration before enabling it and keep hot-cache content concise, current, and appropriate for automatic loading. <br>


## Reference(s): <br>
- [Memory Management Skill](https://clawhub.ai/aaron-he-zhu/memory-management) <br>
- [Project Homepage](https://github.com/aaron-he-zhu/seo-geo-claude-skills) <br>
- [Examples](references/examples.md) <br>
- [Hot Cache Template](references/hot-cache-template.md) <br>
- [Promotion and Demotion Rules](references/promotion-demotion-rules.md) <br>
- [Update Triggers and Cross-Skill Integration](references/update-triggers-integration.md) <br>
- [Wiki Layer Runbook](references/wiki-runbook.md) <br>
- [GDPR / CCPA Purge Log Schema](references/gdpr-purge-log-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, plans, summaries, and proposed file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory update plans, hot-cache changes, handoff summaries, archive guidance, wiki maintenance steps, and privacy purge records.] <br>

## Skill Version(s): <br>
9.9.9 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
