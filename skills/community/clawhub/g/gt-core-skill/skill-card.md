## Description:

Use this skill when the user needs to work with Gumtree in a real Chrome browser session to check login state, log in or out, search listings, read recommendations, favourites, detail pages and messages, favourite listings, and start the post-ad category flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluebluebbb](https://clawhub.ai/user/bluebluebbb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent operate Gumtree through a real Chrome session for listing search, account-state checks, favourites, messages, detail extraction, and category selection for posting ads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Chrome extension and bridge can operate an authenticated Gumtree session.

Mitigation: Use a dedicated browser profile, install the extension only for intended sessions, and stop the bridge when finished.

Risk: Login credentials may be exposed when passed as command-line arguments.

Mitigation: Avoid passing real passwords on the command line when possible and do not repeat credential-bearing commands in summaries or logs.

Risk: Message sending, favouriting, logout, and post-ad navigation are real account actions.

Mitigation: Review command inputs before execution and confirm account-changing actions with the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluebluebbb/skills/gt-core-skill)
- [uv documentation](https://docs.astral.sh/uv/)
- [Gumtree favourites page](https://www.gumtree.com/my-account/favourites)
- [Gumtree messages page](https://www.gumtree.com/manage/messages)
- [Gumtree category suggestion endpoint](https://my.gumtree.com/api/category/suggest)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results should preserve important JSON fields; Gumtree actions run against a live browser session.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
