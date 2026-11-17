## Description:

Fetch the latest AI daily brief from imjuya/juya-ai-daily (GitHub) and return the Overview (summary) section.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunter-wrynn](https://clawhub.ai/user/hunter-wrynn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch the latest public Juya AI Daily brief from GitHub and return only the Overview section. It also guides optional follow-up requests for detailed explanations of numbered items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to GitHub and can optionally send a GitHub token for rate-limit handling.

Mitigation: Use no token when possible, or use a low-scope token created for this purpose.

Risk: The skill body uses node to parse GitHub API results, but the metadata only declares curl.

Mitigation: Confirm node is available in the agent runtime before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hunter-wrynn/skills/juya-ai-daily-skills)
- [GitHub BACKUP contents API used by the skill](https://api.github.com/repos/imjuya/juya-ai-daily/contents/BACKUP?ref=master)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with the latest date, Overview section, and optional follow-up prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to GitHub; optionally uses GITHUB_TOKEN or GH_TOKEN for rate limits.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
