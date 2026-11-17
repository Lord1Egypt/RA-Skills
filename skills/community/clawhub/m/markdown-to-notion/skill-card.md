## Description:

Converts Markdown content into Notion API-compatible page content through a Xiaobenyang API-backed tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to convert Markdown into JSON page content for Notion integrations. It is appropriate when sending the Markdown to the Xiaobenyang service is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Markdown content to the remote Xiaobenyang API.

Mitigation: Use it only for content that may be processed by that service, and avoid private or regulated documents unless remote processing has been approved.

Risk: The skill stores the Xiaobenyang API key in a local .env file.

Mitigation: Treat the .env file as sensitive, restrict file access, and rotate or scope the API key according to your credential policy.

Risk: The security summary notes mismatched Gaokao/template references that make the skill scope unclear.

Mitigation: Review the endpoint settings, requested tool name, and source text before deployment to confirm the skill performs only the intended Markdown-to-Notion conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/markdown-to-notion)
- [Xiaobenyang service](https://xiaobenyang.com)
- [Xiaobenyang API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [JSON response data summarized for the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY credential and remote Xiaobenyang API processing.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
