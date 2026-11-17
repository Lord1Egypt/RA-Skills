## Description:

Provides a command-line interface for GuanYuan Data APIs with token management, card data retrieval, and JSON or CSV export with metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackeylee007](https://clawhub.ai/user/jackeylee007)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and data operators use this skill to configure GuanYuan API access, retrieve card data, and export results for analysis or downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account passwords and API tokens can be stored under ~/.guanyuan or passed through shell commands, which may expose secrets through files, shell history, or logs.

Mitigation: Prefer interactive token entry or a dedicated secret manager, avoid placing real tokens directly in shell commands, and restrict permissions on ~/.guanyuan and its files.

Risk: The configured baseUrl controls where credentials and tokens are sent.

Mitigation: Verify the GuanYuan baseUrl before login, token use, or data export, and use trusted HTTPS endpoints only.

Risk: CSV and metadata exports may overwrite existing files and may contain sensitive business data.

Mitigation: Export to a controlled local directory, avoid shared or source-controlled folders, and check filenames before running export commands.

## Reference(s):

- [GuanYuan Data API Skill README](references/README.md)
- [User Login API](https://api.guandata.com/apidoc/docs-site/345092/710/api-3470502)
- [Get Card Data API](https://api.guandata.com/apidoc/docs-site/345092/710/api-3471043)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, API JSON responses, CSV files, and metadata JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV export can write an output CSV and a matching _meta.json metadata file; command output may also be printed to stdout.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
