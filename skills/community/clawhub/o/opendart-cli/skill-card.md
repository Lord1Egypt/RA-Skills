## Description:

OpenDART CLI lets agents and developers query Korea FSS DART OpenAPI data from the terminal for company identifiers, disclosures, company profiles, financial statements, shareholder information, and source document downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, financial analysts, and agent builders use this skill to retrieve Korean corporate disclosure, company, financial statement, shareholder, and document data as structured CLI output for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenDART API credentials could be exposed if supplied outside the documented environment variable.

Mitigation: Set OPENDART_API_KEY through the documented environment variable and avoid passing credentials through shell history, logs, or command arguments.

Risk: Corp-code cache files may persist Korean company lookup data on the local machine.

Mitigation: Use OPENDART_CACHE_DIR to place the cache in an approved directory and refresh or remove cached data according to local retention requirements.

Risk: Document download commands write files to the path selected by the user.

Mitigation: Choose an expected output path, review downloaded ZIP files before further processing, and avoid overwriting important local files.

## Reference(s):

- [OpenDART CLI on ClawHub](https://clawhub.ai/chloepark85/skills/opendart-cli)
- [OpenDART](https://opendart.fss.or.kr)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON-oriented output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENDART_API_KEY; Korean CLI messages are expected; corp-code data may be cached locally; document downloads write to the user-selected path.]

## Skill Version(s):

0.1.0 (source: server release metadata, SKILL.md frontmatter, pyproject.toml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
