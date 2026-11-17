## Description:

Parses natural-language search requests into ES search parameters, calls an ES search API for social media and news data, and returns formatted results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urhd528](https://clawhub.ai/user/urhd528)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agent operators use this skill to search social media and news content by keyword, platform, sentiment, and date range from a natural-language request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling and authentication documentation need review before installation.

Mitigation: Use only with a trusted local ES API service, confirm the required authentication flow, and review the skill before deployment.

Risk: Credentials may be stored or displayed in plaintext configuration.

Mitigation: Use a low-scope app_key that can be rotated, avoid storing unnecessary tokens, and do not run --show-config in shared logs or screen-sharing sessions.

Risk: Dependency versions are not pinned.

Mitigation: Pin dependencies and review updates before installing the skill in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urhd528/skills/gsdata-data-search)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown search results, JSON parameter previews, or plain-text status and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a trusted local ES API service and read or write config.json for app_key and optional token settings.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
