## Description:

Hum is an AI content writing skill for X and LinkedIn that crawls feed sources, sends digests, researches ideas, drafts posts in the user's voice, and supports approved publishing and engagement actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jyek](https://clawhub.ai/user/jyek)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and marketing or developer advocates use Hum to monitor content sources, brainstorm and research ideas, draft X and LinkedIn content in their own voice, and manage publishing or engagement after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles social-account credentials, browser sessions, feed history, drafts, and generated images.

Mitigation: Install only in trusted environments, keep credentials scoped, store credential files with restrictive permissions such as chmod 600, and avoid sharing the configured data directory.

Risk: Publishing, following, commenting, and replying can affect live X or LinkedIn accounts.

Mitigation: Review every publish, follow, comment, and reply action before execution, and require explicit user approval for outbound account actions.

Risk: The security evidence reports file, network, dashboard, environment-forwarding, and dependency-pinning weaknesses.

Mitigation: Keep any dashboard limited to localhost, treat crawled knowledge sources as untrusted, review source configuration before crawling, and address the reported weaknesses before broader deployment.

Risk: The skill can make outbound calls to feed, social, Telegram, and image-generation providers.

Mitigation: Configure only the provider credentials that are needed, disable scheduled digest delivery unless desired, and review outbound destinations before enabling automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jyek/skills/hum-writer)
- [SKILL.md](artifact/SKILL.md)
- [COMMANDS.md](artifact/COMMANDS.md)
- [LOOP.md](artifact/LOOP.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, plain-text digests, JSON files, generated drafts, generated image assets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can publish posts and comments through configured X and LinkedIn credentials after user approval; can call configured feed, social, and image-generation providers.]

## Skill Version(s):

0.2.1 (source: server release metadata and artifact/version.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
