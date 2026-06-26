## Description: <br>
Helps an agent create, format, preview, and publish WeChat public account content through a configured SaaS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lufeng321](https://clawhub.ai/user/lufeng321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and developers use this skill to manage materials, draft articles, apply WeChat-compatible templates, generate cover and social copy assets, check quotas, and publish or distribute reviewed content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language triggers and publishing actions can affect a connected WeChat account unintentionally. <br>
Mitigation: Require manual review of the exact article, assets, template, target account, and destination platforms before publish, distribute, or clear-materials actions. <br>
Risk: The skill depends on a configured SaaS endpoint and an API key with publishing permissions. <br>
Mitigation: Install only when the publisher and endpoint are trusted, and use a dedicated, revocable API key rather than a shared credential. <br>
Risk: Drafts, source articles, materials, and generated assets may be sent to the configured SaaS service. <br>
Mitigation: Avoid confidential drafts or sensitive account material unless the service and account controls are approved for that content. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lufeng321/lanreneditor-pro) <br>
- [Publisher profile](https://clawhub.ai/user/lufeng321) <br>
- [Configured SaaS platform](https://open.tyzxwl.cn) <br>
- [Template designer](https://open.tyzxwl.cn/website/template-designer.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown, HTML snippets, JSON API payloads, interactive choices, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create drafts, previews, cover assets, social copy, pipeline job IDs, publish task IDs, and account-affecting actions through the configured endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
