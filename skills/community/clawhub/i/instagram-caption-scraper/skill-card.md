## Description:

Scrapes and returns the caption from any public Instagram post or reel URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rdk14](https://clawhub.ai/user/rdk14)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when an Instagram post or reel URL is provided and the user wants the caption extracted before summarization, translation, rewriting, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact suggests adding Instagram login credentials to the script for authenticated access, which could expose plaintext credentials and broaden access beyond public posts.

Mitigation: Use the skill only for public Instagram links; do not embed usernames or passwords in the script, and require protected secret or session handling with explicit consent if authenticated access is ever added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rdk14/skills/instagram-caption-scraper)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text string prefixed with CAPTION or ERROR, with caption metadata on success.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public Instagram post and reel captions; private, deleted, invalid, or inaccessible posts are reported as errors.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
