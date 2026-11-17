## Description:

Extract X (Twitter) data including user profiles, posts, followers, followings, media, and search results.

This skill is for research and development only.

## Publisher:

[hardbrick21](https://clawhub.ai/user/hardbrick21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use Omni-X to retrieve X/Twitter profile, post, follower, following, media, and search data through a Python skill interface. Authenticated features require an X/Twitter session token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users and agents to handle live X/Twitter session credentials.

Mitigation: Prefer guest mode or a dedicated low-risk account, store tokens in environment variables or a secret manager, and avoid saved sessions.

Risk: Authenticated extraction and large result counts can increase account, rate-limit, privacy, and terms-of-service risk.

Mitigation: Use small result counts, add delays and backoff, avoid redistributing extracted data without authorization, and confirm the use complies with X/Twitter terms and applicable privacy obligations.

Risk: The dependency is unpinned, which can change behavior across installations.

Mitigation: Pin dependency versions and review dependency updates before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hardbrick21/skills/omni-x)
- [AI Agent Integration Guide](references/AI_AGENT_GUIDE.md)
- [Installation and Usage Guide](references/INSTALLATION.md)
- [Login Guide](references/LOGIN_GUIDE.md)
- [TweeterPy Repository](https://github.com/iSarabjitDhiman/TweeterPy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and Python examples; runtime skill calls return structured Python dictionaries containing success, data, count, pagination cursor, skill name, parameters, or error fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guest mode supports profile and tweet retrieval; follower, following, media, and search functions require authentication and may include paginated results.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
