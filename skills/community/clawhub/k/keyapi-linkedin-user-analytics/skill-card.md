## Description:

Discover, profile, and analyze LinkedIn users, including profiles, contact information, work experience, education, skills, publications, certifications, honors, recommendations, interests, posts, comments, and videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to retrieve LinkedIn professional profile data, inspect career and content activity, and build structured people-research reports or shortlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive LinkedIn profile and contact data that may be stored in local cache files.

Mitigation: Use the skill only for authorized research, clear or relocate .keyapi-cache after use, and avoid retaining personal data longer than necessary.

Risk: A KeyAPI token is required and may be stored in a plaintext .env file if entered interactively.

Mitigation: Prefer environment variables or a secrets manager, use a scoped or disposable token, and avoid interactive token entry unless plaintext local storage is acceptable.

Risk: Overriding KEYAPI_SERVER_URL can send API requests and tokens to a different MCP endpoint.

Mitigation: Use the default KeyAPI endpoint unless the replacement endpoint is explicitly trusted and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-linkedin-user-analytics)
- [KeyAPI website](https://keyapi.ai/)
- [KeyAPI LinkedIn MCP endpoint](https://mcp.keyapi.ai/linkedin/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache API responses locally and may save JSON output when the runner is called with an output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
