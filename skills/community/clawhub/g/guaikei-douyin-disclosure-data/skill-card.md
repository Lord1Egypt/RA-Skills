## Description:

Provides command-line access to Douyin public search, creator post, comment, and hot-topic data for content research and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content operations teams use this skill to query public Douyin content, creator posts, comments, and current hot topics for competitive research, content planning, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends configured tokens and requests to the vendor API.

Mitigation: Use only a token approved for this vendor service, keep it in the environment, and rotate it if logs or shell history may have exposed it.

Risk: Successful search, post, and comment commands save social-media data that can include comments, user identifiers, URLs, and query history.

Mitigation: Restrict access to generated logs, delete them when no longer needed, and avoid redistributing collected data without review.

Risk: Outputs can include media or play URLs even though the skill documentation says it is not for downloading videos.

Mitigation: Review JSON results before sharing them and do not use exposed URLs to download, republish, or distribute media.

Risk: The security verdict requires review because the skill saves collected public data by default and has weak token/error handling.

Mitigation: Review the skill before installation and use it only for clear, public Douyin data requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-disclosure-data)
- [Usage documentation](artifact/readme.md)
- [Command options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Search request schema](artifact/assets/search_cli_req.schema.json)
- [Search response schema](artifact/assets/search_cli_resp.schema.json)
- [Post response schema](artifact/assets/post_cli_resp.schema.json)
- [Comment response schema](artifact/assets/comment_cli_resp.schema.json)
- [Hot topic response schema](artifact/assets/hot_cli_resp.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON envelopes on stdout with logs on stderr and saved JSON result files for search, post, and comment commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or later and a GUAIKEI_API_TOKEN; individual commands support limits up to 10000 records.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact package.json, and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
