## Description: <br>
Manage Miniflux via its REST API for listing feeds and entries, creating or removing subscriptions, searching articles, managing categories, and marking entries as read or unread. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dorogoy](https://clawhub.ai/user/dorogoy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and feed-reader users use this skill to operate a Miniflux account from an agent workflow, including feed management, entry search, category management, and read-state updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users could copy the README's example Miniflux URL and send token-backed requests to the wrong server. <br>
Mitigation: Set MINIFLUX_URL only to a trusted Miniflux instance that the user controls or intentionally uses. <br>
Risk: Commands that delete feeds, update feeds, mark entries read, or toggle bookmarks make live changes to the connected Miniflux account. <br>
Mitigation: Review command arguments before execution and use a least-privilege API token where supported. <br>
Risk: Installing Python dependencies directly into a system environment can affect other Python tooling. <br>
Mitigation: Install the miniflux Python package in a virtual environment when possible. <br>


## Reference(s): <br>
- [Miniflux API documentation](https://miniflux.app/docs/api.html) <br>
- [ClawHub skill page](https://clawhub.ai/dorogoy/miniflux-skill) <br>
- [Publisher profile](https://clawhub.ai/user/dorogoy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text output from Miniflux API operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the miniflux Python package, MINIFLUX_URL, and MINIFLUX_TOKEN.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata and changelog, released 2026-02-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
