## Description:

Publish blog posts to Medium via GitHub Pages + URL import; no API token required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylnhari](https://clawhub.ai/user/ylnhari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and teams use this skill to create Medium-ready blog drafts from a topic, outline, or source content. It writes constrained HTML, publishes it through the user's GitHub Pages site, imports it into Medium, and stops at draft review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update public GitHub repositories and publish draft source pages publicly.

Mitigation: Confirm the target owner, repo, branch, and public URL before each run, and avoid using sensitive or unpublished content.

Risk: The workflow uses the user's authenticated GitHub and Medium sessions.

Mitigation: Run only in trusted workspaces and confirm authentication state before allowing repository or browser actions.

Risk: Medium draft editor URLs may be exposed if committed to a public repository.

Mitigation: Review post metadata before pushing and do not commit Medium draft editor URLs to public repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylnhari/skills/medium-blog-post-creator)
- [Skill homepage](https://github.com/ylnhari/openclaw-skills/tree/main/skills/medium-blog-post-creator)
- [HTML standards for Medium's URL importer](references/html-standards.md)
- [Persistent configuration](references/configuration.md)
- [Post HTML template](assets/post-template.html)
- [Metadata sidecar template](assets/meta.template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus generated HTML and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates public GitHub Pages source pages and a Medium draft URL; requires authenticated gh, git, and a Medium browser session.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
