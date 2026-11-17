## Description:

Exports comments from the user's logged-in WeChat public account into a local, article-grouped Markdown archive and JSON summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatmind](https://clawhub.ai/user/fatmind)

### License/Terms of Use:

MIT-0

## Use Case:

WeChat public-account operators use this skill to archive comments on their own posts and review reader feedback from the account currently logged in to Chrome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser automation channel operates in a Chrome session already logged in to the public-account dashboard.

Mitigation: Use only a trusted local browser relay and confirm the intended account is logged in before exporting.

Risk: The local archive can contain reader nicknames, comment text, timestamps, regions, and account details.

Mitigation: Keep exported files in a protected location and limit sharing and retention according to your privacy needs.

Risk: The bundled optional wc3-code.mjs helper can send supplied content to a local LLM service.

Mitigation: Do not invoke the helper with sensitive content unless you understand and trust that service; it is not needed for the documented export.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fatmind/skills/gzh-comment-export)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Local comments.md grouped by article, index.json with counts and export status, and a JSON status line on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes author, comment text, time, and available region; incomplete exports are marked partial.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
