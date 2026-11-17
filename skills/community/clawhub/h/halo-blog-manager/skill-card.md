## Description:

Manage Halo CMS blogs through authenticated API operations for posts, categories, tags, comments, users, and media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siyrs](https://clawhub.ai/user/siyrs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to administer a Halo CMS blog from an agent, including drafting or publishing posts, managing taxonomy, moderating comments, checking basic site data, and uploading media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses administrative Halo credentials and session cookies that can grant broad access to a blog.

Mitigation: Use an HTTPS-only blog URL, restrict access to ~/halo-manager/config.json and ~/halo-manager/session.json, and remove those files when the session is no longer needed.

Risk: The skill can publish, update, or delete blog content, taxonomy, comments, and media.

Mitigation: Manually confirm the target resource and requested action before allowing publish, update, delete, approval, or upload operations.

Risk: The security verdict is suspicious because credentials and session cookies are stored insecurely.

Mitigation: Install only when that storage model is acceptable for the local environment and avoid reused passwords.

## Reference(s):

- [Halo API Reference](artifact/references/api-reference.md)
- [Halo Manager Examples](artifact/references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/siyrs/skills/halo-blog-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request summaries, JSON examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Halo credential and session files when setup or authentication is performed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
