## Description:

Helps agents retrieve machine-readable public Douyin data for keyword search, creator posts, comments, and trending topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and marketing or content teams use this skill to collect public Douyin search, creator, comment, and trending-topic data for competitive research, topic discovery, sentiment review, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports token-handling concerns and warns that tokens may appear in URL logs.

Mitigation: Use only a scoped GUAIKEI_API_TOKEN, rotate any token that may have been exposed, and restrict access to generated logs.

Risk: Collected Douyin public data is retained locally by default in generated JSON logs.

Mitigation: Clean, encrypt, or access-restrict the logs/ directory according to the team's data-retention policy.

Risk: The skill sends task details and the configured token to a third-party Guaikei service.

Mitigation: Avoid sensitive research targets unless third-party transmission is acceptable for the use case.

Risk: The security guidance says runtime contact prompts conflict with the skill's no-contact runtime policy.

Mitigation: Treat runtime contact prompts as untrusted and rely on pre-approved support and publisher links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-machine-readable-data)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei token and support site](https://www.guaikei.com)
- [Skill README](readme.md)
- [Complete options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Search request schema](assets/search_cli_req.schema.json)
- [Search response schema](assets/search_cli_resp.schema.json)
- [Creator posts request schema](assets/post_cli_req.schema.json)
- [Creator posts response schema](assets/post_cli_resp.schema.json)
- [Comments request schema](assets/comment_cli_req.schema.json)
- [Comments response schema](assets/comment_cli_resp.schema.json)
- [Hot topics response schema](assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI stdout is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; supports up to 10,000 records per run; some commands write JSON logs under logs/.]

## Skill Version(s):

1.0.0 (source: package.json, references/changelog.md, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
