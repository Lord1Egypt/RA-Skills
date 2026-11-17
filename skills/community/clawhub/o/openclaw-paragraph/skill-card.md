## Description:

OpenClaw skill enabling automated creation, retrieval, subscriber management, and tokenized engagement with Web3-native blog posts on Paragraph.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claireaicodes](https://clawhub.ai/user/claireaicodes)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, DAOs, Web3 project teams, and developers use this skill to automate Paragraph publishing workflows, manage subscribers, inspect publications and posts, and work with tokenized post engagement from OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing API calls can be redirected if PARAGRAPH_API_BASE_URL is changed.

Mitigation: Keep PARAGRAPH_API_BASE_URL fixed to the official Paragraph API unless a trusted reviewer approves a controlled test endpoint.

Risk: Post creation, newsletter sending, welcome emails, and subscriber imports can create public or user-facing effects.

Mitigation: Require explicit user approval before running publishing or subscriber-management actions.

Risk: Subscriber CSV import can upload local file contents selected by path.

Mitigation: Use only verified subscriber CSV files and avoid running the skill where sensitive local files are accessible to the agent process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/claireaicodes/skills/openclaw-paragraph)
- [Publisher Profile](https://clawhub.ai/user/claireaicodes)
- [Paragraph API Reference](https://paragraph.com/docs/api-reference)
- [Paragraph](https://paragraph.com)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, API responses, guidance]

**Output Format:** [JSON API results and Markdown-oriented publishing content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Paragraph API credentials and publication configuration; some operations create public posts or send subscriber emails.]

## Skill Version(s):

1.2.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
