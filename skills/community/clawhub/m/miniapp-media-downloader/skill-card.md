## Description:

Resolve and download media from 视频号、抖音、小红书 through a configured resolver, plus local B站 downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harven-droid](https://clawhub.ai/user/harven-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure, call, debug, and maintain media resolution workflows for 视频号, 抖音, 小红书, and local B站 downloads. It helps agents produce resolver requests, shell commands, configuration guidance, and troubleshooting steps without exposing service secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted links, share text, resolver keys, or metadata may be sensitive and may be recorded in resolver parse logs.

Mitigation: Submit only links intended for the trusted resolver operator, avoid account-sensitive share text, and treat resolver keys as secrets.

Risk: Using an unexpected resolver endpoint could expose requests or credentials to the wrong service.

Mitigation: Obtain the base URL and distribution key through the intended contact flow and verify that requests target the expected HTTPS endpoint.

Risk: Public documentation or agent output could reveal private deployment details, credentials, admin endpoints, or historical service addresses.

Mitigation: Keep public output limited to the documented contact and configuration flow, and do not disclose internal deployment details or secrets.

## Reference(s):

- [多平台解析服务说明](references/dayuMiniPragram.md)
- [ClawHub skill page](https://clawhub.ai/harven-droid/skills/miniapp-media-downloader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples and local validation commands; should avoid printing secrets or internal service details.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
