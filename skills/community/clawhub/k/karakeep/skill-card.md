## Description:

Manage bookmarks and links in a Karakeep instance. Use when the user wants to save links, list recent bookmarks, or search their collection. Triggers on phrases like "hoard this link", "save to karakeep", or "search my bookmarks".

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayphen](https://clawhub.ai/user/jayphen)

### License/Terms of Use:


## Use Case:

Developers and other Karakeep users can use this skill to configure access to a Karakeep instance, save links, list recent bookmarks, and search bookmark collections from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Karakeep API key and may access sensitive bookmark data.

Mitigation: Use a scoped token when possible, keep the token out of shared logs, and restrict permissions on `~/.config/karakeep/config.json`.

Risk: A hardcoded default instance URL may send requests to an unintended Karakeep service if the user does not configure a URL.

Mitigation: Configure an explicit HTTPS Karakeep instance URL before using the skill and review the saved config before running commands.

Risk: The CLI fetches the `requests` dependency through `uv --with requests` during normal use.

Mitigation: Pin or preinstall dependencies in a controlled environment for production or sensitive deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayphen/skills/karakeep)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and a Karakeep instance URL plus API key.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
