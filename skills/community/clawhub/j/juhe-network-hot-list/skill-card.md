## Description:

Queries real-time hot-search rankings across major Chinese platforms, including Weibo, Douyin, Kuaishou, Zhihu, Baidu, Toutiao, and Bilibili, using the Juhe network hot-list API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and present current trending topics from multiple Chinese social and search platforms. Agents can call the included Python script or the documented API and return ranked results in a concise table or JSON-backed summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key may be exposed because the script sends it to Juhe over plaintext HTTP.

Mitigation: Review the endpoint before use and change it to HTTPS when supported by the provider.

Risk: API keys may be captured in shell history or process listings when passed with the --key command-line option.

Mitigation: Set JUHE_HOTSEARCH_KEY as an environment variable instead of passing the key on the command line.

Risk: A local scripts/.env file can accidentally disclose the API key if committed or shared.

Mitigation: Keep scripts/.env out of source control and deployment bundles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-network-hot-list)
- [Juhe network hot-list API documentation](https://www.juhe.cn/docs/api/id/739)
- [Juhe data service](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and tabular or JSON hot-list results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_HOTSEARCH_KEY API key; supports --limit, --detail, and --key options.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
