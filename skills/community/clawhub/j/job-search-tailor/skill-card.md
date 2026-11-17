## Description:

Job Search Tailor helps users search LinkedIn job listings, deduplicate results, and match each posting to a tailored resume archetype.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericshi123](https://clawhub.ai/user/ericshi123)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to configure recurring job searches, track previously seen listings, and select or create resume archetypes for each relevant posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores resume-derived files and job history locally under ~/.job-search or configured paths.

Mitigation: Review config.json paths before running and manually approve generated archetype or resume files before relying on them.

Risk: Untrusted job pages and configurable paths can influence local file writes and resume tailoring decisions.

Mitigation: Inspect fetched job content, tracking_file, and archetypes_dir settings before allowing the skill to create or update local files.

Risk: Google Docs integration is not implemented in v1 but could involve credentials if configured later.

Mitigation: Keep google_docs_enabled false unless deliberately setting up credentials, and audit any resume URLs before sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericshi123/skills/job-search-tailor)
- [Archetypes Guide](references/archetypes-guide.md)
- [Config Guide](references/config-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest with local file paths, JSON configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local resume archetype markdown files, config.json, and shared job tracking JSON under configured paths.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
