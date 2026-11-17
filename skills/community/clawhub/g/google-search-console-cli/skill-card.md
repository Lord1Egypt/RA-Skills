## Description:

Use this skill to install, configure, authenticate, operate, and troubleshoot the `gsc` CLI for Google Search Console workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmadeleidev](https://clawhub.ai/user/nmadeleidev)

### License/Terms of Use:


## Use Case:

Developers, site owners, and SEO operators use this skill to set up Google Cloud OAuth credentials, authenticate the `gsc` CLI, manage Search Console properties and sitemaps, inspect URLs, query analytics, and troubleshoot configuration or API connectivity issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth client secrets and local credential files can authorize access to Google Search Console properties if exposed.

Mitigation: Keep downloaded OAuth client JSON private, protect `~/.config/gsc-cli/credentials.json` and any configured credential paths, and avoid sharing command output that reveals sensitive paths or account details.

Risk: Using broad OAuth scopes can allow write actions such as sitemap submission or deletion when only reporting is needed.

Mitigation: Prefer the CLI's `--readonly` authentication option for reporting and analytics workflows, and re-authenticate without readonly scope only when write operations are required.

Risk: Installing an untrusted CLI package can run code on the user's machine.

Mitigation: Confirm trust in the `google-search-console-cli` package source before installing it with `pipx`, `pip`, or editable source commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nmadeleidev/skills/google-search-console-cli)
- [Publisher profile](https://clawhub.ai/user/nmadeleidev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that authenticate against Google Search Console, read or write local credential files, and emit table, JSON, or CSV command outputs depending on the CLI option selected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
