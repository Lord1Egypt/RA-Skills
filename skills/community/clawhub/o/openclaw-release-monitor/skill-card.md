## Description: <br>
Check OpenClaw release notes from GitHub, show highlights and categorized changes translated to the user's language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tjefferson](https://clawhub.ai/user/tjefferson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to check latest, recent, or specific OpenClaw release notes, compare versions, and get concise categorized upgrade highlights in their language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured GitHub token could be broader than needed for public release-note lookups. <br>
Mitigation: Use a token with minimal or no special scopes, or omit GITHUB_TOKEN when the unauthenticated GitHub API rate limit is sufficient. <br>
Risk: GitHub API rate limits or network failures can prevent current release retrieval. <br>
Mitigation: Surface the API error, suggest GITHUB_TOKEN only for rate-limit relief, and link the user to the release page when release body data is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tjefferson/openclaw-release-monitor) <br>
- [OpenClaw GitHub releases API](https://api.github.com/repos/openclaw/openclaw/releases) <br>
- [OpenClaw GitHub release example](https://github.com/openclaw/openclaw/releases/tag/v2026.3.31) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with headings, bullets, tables, and inline links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May translate release-note summaries into the user's language while preserving technical terms and module prefixes.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
