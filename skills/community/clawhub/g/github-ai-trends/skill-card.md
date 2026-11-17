## Description:

Generate GitHub AI trending project reports as formatted text leaderboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toller892](https://clawhub.ai/user/toller892)

### License/Terms of Use:


## Use Case:

Developers, researchers, and external users use this skill to fetch recently active AI, ML, and LLM repositories from GitHub and produce a concise leaderboard for chat display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make GitHub API requests and may use an optional GitHub token.

Mitigation: Run without a token when possible, or provide a fine-grained short-lived token through the GITHUB_TOKEN environment variable.

Risk: Repository names, descriptions, and links in the generated leaderboard come from GitHub and should be treated as untrusted content.

Mitigation: Review leaderboard entries before acting on links or repository descriptions.

## Reference(s):

- [GitHub AI Trends ClawHub skill page](https://clawhub.ai/toller892/skills/github-ai-trends)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown leaderboard by default, with optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports daily, weekly, and monthly periods; limit controls the number of repositories returned.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
