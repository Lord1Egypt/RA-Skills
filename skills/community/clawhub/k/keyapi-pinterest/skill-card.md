## Description:

Discover and analyze Pinterest users, pins, boards, followers, and following through the KeyAPI REST API using live official docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to turn Pinterest research requests into documentation-guided KeyAPI workflows for account discovery, profile inspection, board and pin audits, and follower or following analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup helper can store a KeyAPI token in a shell profile as plaintext.

Mitigation: Prefer setting KEYAPI_TOKEN only for the current shell session, avoid sharing tokens in prompts or command arguments, and confirm the target shell profile before persistence.

Risk: Helper scripts make live KeyAPI requests and repeated identical commands call the API again.

Mitigation: Review generated commands before execution, confirm broad report scope before multi-call workflows, and use saved output files only when complete data is needed.

Risk: User-controlled --profile, --body-file, --image-file, or --output-file paths can read from or write to local files.

Mitigation: Do not let untrusted prompts choose file paths; inspect paths before running helper commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xyzzero/skills/keyapi-pinterest)
- [KeyAPI Docs Index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI Pinterest Docs](https://docs.keyapi.ai/en/pinterest/)
- [KeyAPI Authentication](https://docs.keyapi.ai/overview/authentication#bearer-authentication)
- [Global Rules](references/global-rules.md)
- [Scenario Cards](references/scenarios.md)
- [Routing Policy](references/routing-policy.md)
- [Pinterest Rules](references/pinterest-rules.md)
- [Pinterest Profile Module Rules](references/pinterest-profile-rules.md)
- [Pinterest Content Module Rules](references/pinterest-content-rules.md)
- [Pinterest Network Module Rules](references/pinterest-network-rules.md)
- [Setup And Auth](references/setup-and-auth.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and optional JSON result files when the user asks to save API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs separate observed KeyAPI facts from analysis and may include setup commands when authentication is unavailable.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
